"""Byggskript för avfallskonsulten.se.

Läser sidorna i src/sidor/, sätter in header/footer/cookie-banner från src/mallar/,
gör bilder i webp i flera storlekar, skapar JSON-LD, sitemap.xml och robots.txt,
och skriver den färdiga sajten till docs/ (den mappen publicerar GitHub Pages).

Kör:  python build.py
"""
import json
import os
import re
import shutil
import sys
from datetime import date
from html import escape, unescape
from pathlib import Path

from PIL import Image

# ---------------------------------------------------------------- inställningar
STAGING = True  # True = spärrad för Google (noindex + robots Disallow). Sätt False när sajten går live.
SITE_URL_LIVE = "https://avfallskonsulten.se"
SITE_URL_STAGING = "https://villestrada.github.io/avfallskonsulten-web"
SITE_URL = SITE_URL_STAGING if STAGING else SITE_URL_LIVE
GTM_ID = "GTM-KDPBR22"  # laddas först efter cookie-samtycke

FORETAG = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "@id": SITE_URL_LIVE + "/#foretag",
    "name": "Avfallskonsulten i huvudstaden AB",
    "alternateName": "Avfallskonsulten",
    "url": SITE_URL_LIVE + "/",
    "logo": SITE_URL_LIVE + "/bilder/logga.svg",
    "image": SITE_URL_LIVE + "/bilder/og-hero_lastbil.jpg",
    "telephone": "+46868427888",
    "email": "info@avfallskonsulten.se",
    "vatID": "SE559128037401",
    "taxID": "559128-0374",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Solkraftsvägen 14 A",
        "postalCode": "135 70",
        "addressLocality": "Stockholm",
        "addressCountry": "SE",
    },
    "areaServed": [
        {"@type": "City", "name": n}
        for n in ["Stockholm", "Sundbyberg", "Järfälla", "Täby", "Lidingö", "Sollentuna", "Norrtälje", "Solna", "Danderyd"]
    ],
    "priceRange": "$$",
    "sameAs": [
        "https://www.instagram.com/avfallskonsulten/",
        "https://www.facebook.com/avfallskonsulten",
        "https://www.reco.se/avfallskonsulten-i-huvudstaden-ab",
    ],
}

ROT = Path(__file__).resolve().parent
SRC = ROT / "src"
UT = ROT / "docs"
BILD_BREDDER = (480, 800, 1200, 1600)
LOGO_BREDDER = (240, 480)

fel = []
varningar = []


# ---------------------------------------------------------------- hjälpfunktioner
def las(p):
    return Path(p).read_text(encoding="utf-8")


def front_matter(text):
    """Returnerar (dict, body). Front matter = rader med 'nyckel: värde' mellan två '---'."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for rad in m.group(1).splitlines():
        if ":" in rad:
            k, v = rad.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, text[m.end():]


def inkludera(html):
    """Byter ut {{include fil.html}} mot innehållet i src/mallar/fil.html."""
    def ers(m):
        return inkludera(las(SRC / "mallar" / m.group(1)))
    return re.sub(r"\{\{include ([\w.\-]+)\}\}", ers, html)


_bildcache = {}


def gor_bild(namn, bredder):
    """Skapar webp-varianter av src/bilder/<namn>.* i docs/bilder/. Returnerar (bredd, höjd, [(w, fil)...])."""
    if namn in _bildcache:
        return _bildcache[namn]
    kand = [p for p in (SRC / "bilder").iterdir() if p.stem == namn and p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")]
    if not kand:
        fel.append(f"Bild saknas: src/bilder/{namn}.*")
        return None
    kalla = kand[0]
    im = Image.open(kalla)
    w0, h0 = im.size
    har_alfa = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    im = im.convert("RGBA" if har_alfa else "RGB")
    (UT / "bilder").mkdir(parents=True, exist_ok=True)
    varianter = []
    for w in bredder:
        if w > w0 and w != bredder[0]:
            continue
        w = min(w, w0)
        h = round(h0 * w / w0)
        ut = UT / "bilder" / f"{namn}-{w}.webp"
        if not ut.exists() or ut.stat().st_mtime < kalla.stat().st_mtime:
            im.resize((w, h), Image.LANCZOS).save(ut, "WEBP", quality=82, method=6)
        varianter.append((w, f"bilder/{namn}-{w}.webp"))
    res = (w0, h0, varianter)
    _bildcache[namn] = res
    return res


def x_bild(m):
    """<x-bild src="namn" alt="..." sizes="..." eager klass="..." logo> -> <img srcset ...>"""
    attr = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
    flaggor = set(re.findall(r'(?:^|\s)(eager|logo)(?=\s|$)', re.sub(r'[\w-]+="[^"]*"', "", m.group(1))))
    namn = attr.get("src", "")
    if "alt" not in attr:
        fel.append(f"Bild utan alt-text: {namn}")
    res = gor_bild(namn, LOGO_BREDDER if "logo" in flaggor else BILD_BREDDER)
    if not res:
        return ""
    w0, h0, varianter = res
    # width/height anges i förhållandet, största varianten som bas
    wmax, _ = varianter[-1]
    hmax = round(h0 * wmax / w0)
    srcset = ", ".join(f"{f} {w}w" for w, f in varianter)
    sizes = attr.get("sizes", "(min-width: 900px) 50vw, 100vw")
    delar = [
        f'src="{varianter[-1][1]}"',
        f'srcset="{srcset}"',
        f'sizes="{sizes}"',
        f'width="{wmax}"',
        f'height="{hmax}"',
        f'alt="{attr.get("alt", "")}"',
        'decoding="async"',
    ]
    if "eager" in flaggor:
        delar.append('fetchpriority="high"')
    else:
        delar.append('loading="lazy"')
    if attr.get("klass"):
        delar.append(f'class="{attr["klass"]}"')
    return "<img " + " ".join(delar) + ">"


def gor_og_bild(namn):
    """1200x630 jpg för Open Graph/Twitter."""
    kand = [p for p in (SRC / "bilder").iterdir() if p.stem == namn and p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")]
    if not kand:
        fel.append(f"OG-bild saknas: {namn}")
        return None
    ut = UT / "bilder" / f"og-{namn}.jpg"
    if not ut.exists() or ut.stat().st_mtime < kand[0].stat().st_mtime:
        im = Image.open(kand[0]).convert("RGB")
        w, h = im.size
        mal = 1200 / 630
        if w / h > mal:
            nw = round(h * mal); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = round(w / mal); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        im.resize((1200, 630), Image.LANCZOS).save(ut, "JPEG", quality=85, optimize=True)
    return f"bilder/og-{namn}.jpg"


def text_av(html):
    t = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", unescape(t)).strip()


def faq_schema(body):
    """Bygger FAQPage-JSON-LD av alla <details class="faq"> i sidan."""
    fragor = []
    for m in re.finditer(r'<details class="faq">(.*?)</details>', body, re.S):
        s = re.search(r"<summary>(.*?)</summary>(.*)", m.group(1), re.S)
        if not s:
            continue
        fragor.append({
            "@type": "Question",
            "name": text_av(s.group(1)),
            "acceptedAnswer": {"@type": "Answer", "text": text_av(s.group(2))},
        })
    if not fragor:
        return None
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": fragor}


def ld_script(obj):
    s = json.dumps(obj, ensure_ascii=False, indent=1)
    json.loads(s)  # validering: måste vara giltig JSON
    return '<script type="application/ld+json">\n' + s.replace("</", "<\\/") + "\n</script>"


def kontrollera_tankstreck(namn, body):
    if "–" in body or "—" in body:
        varningar.append(f"{namn}: innehåller tankstreck, använd komma i stället")


# ---------------------------------------------------------------- bygg
def bygg():
    if UT.exists():
        for p in UT.iterdir():
            if p.name == "bilder":
                continue  # cache för webp-varianter
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    UT.mkdir(exist_ok=True)
    (UT / ".nojekyll").write_text("")

    # statiska filer
    for mapp in ("css", "js", "typsnitt"):
        shutil.copytree(SRC / mapp, UT / mapp, dirs_exist_ok=True)
    # typsnittets @font-face läggs in direkt i style.css (sparar en nätverksrunda)
    css = las(SRC / "css" / "style.css")
    fonts = las(SRC / "typsnitt" / "roboto-lokal.css")
    css = css.replace('@import url("../typsnitt/roboto-lokal.css");', fonts.strip())
    (UT / "css" / "style.css").write_text(css, encoding="utf-8")
    (UT / "typsnitt" / "roboto-lokal.css").unlink()
    (UT / "bilder").mkdir(exist_ok=True)
    for p in (SRC / "bilder").glob("*.svg"):
        shutil.copy(p, UT / "bilder" / p.name)
    shutil.copy(SRC / "bilder" / "favicon.png", UT / "favicon.png")
    shutil.copy(SRC / ".htaccess", UT / ".htaccess")            # 301, 404, headers på Loopia
    shutil.copytree(SRC / "includes", UT / "includes", dirs_exist_ok=True)  # PHP-formulärhanterare

    bas = las(SRC / "mallar" / "bas.html")
    sidor = []
    for fil in sorted((SRC / "sidor").glob("*.html")):
        meta, body = front_matter(las(fil))
        slug = meta.get("slug", fil.stem)
        if slug == "index":
            slug = ""
        utfil = (fil.stem + ".html")
        namn = fil.name
        kontrollera_tankstreck(namn, body)

        for k in ("titel", "beskrivning"):
            if not meta.get(k):
                fel.append(f"{namn}: saknar '{k}' i front matter")
        if len(re.findall(r"<h1[\s>]", body)) != 1:
            fel.append(f"{namn}: ska ha exakt en <h1>")

        body = inkludera(body)
        body = re.sub(r"<x-bild\s+([^>]*?)\s*/?>", x_bild, body)

        canonical = f"{SITE_URL}/{slug}" if slug else f"{SITE_URL}/"
        og_bild = gor_og_bild(meta.get("og_bild", "hero_lastbil"))
        ld = [ld_script(FORETAG)]
        faq = faq_schema(body)
        if faq:
            ld.append(ld_script(faq))

        robots = "noindex,nofollow" if STAGING or meta.get("index") == "nej" else "index,follow"
        html = bas
        html = inkludera(html)
        ers = {
            "titel": escape(meta.get("titel", "")),
            "beskrivning": escape(meta.get("beskrivning", "")),
            "canonical": canonical,
            "og_bild": f"{SITE_URL}/{og_bild}" if og_bild else "",
            "og_typ": "website" if not slug else "article",
            "robots": robots,
            "innehall": body,
            "ld": "\n".join(ld),
            "gtm_id": GTM_ID,
            "ar": str(date.today().year),
            "slug": slug,
            "body_klass": meta.get("body_klass", ""),
            "form_lage": "staging" if STAGING else "live",
        }
        for k, v in ers.items():
            html = html.replace("{{" + k + "}}", v)
        if 'id="boka"' not in body:
            html = html.replace('href="#boka"', 'href="./#boka"')  # sidor utan formulär länkar till startsidans
        rest = re.findall(r"\{\{[^}]+\}\}", html)
        if rest:
            fel.append(f"{namn}: okända platshållare {sorted(set(rest))}")
        (UT / utfil).write_text(html, encoding="utf-8")
        sidor.append({"slug": slug, "fil": utfil, "sitemap": meta.get("sitemap", "ja") == "ja", "mtime": fil.stat().st_mtime})
        print(f"  {utfil:40s} {meta.get('titel','')}")

    # sitemap.xml
    rader = []
    for s in sidor:
        if not s["sitemap"]:
            continue
        loc = f"{SITE_URL}/{s['slug']}" if s["slug"] else f"{SITE_URL}/"
        lastmod = date.fromtimestamp(s["mtime"]).isoformat()
        rader.append(f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod></url>")
    (UT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rader) + "\n</urlset>\n", encoding="utf-8")

    # robots.txt
    if STAGING:
        (UT / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    else:
        (UT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")

    # länkkontroll: interna länkar ska peka på sidor som finns
    finns = {s["fil"] for s in sidor} | {s["slug"] for s in sidor if s["slug"]} | {""}
    saknade = set()
    for s in sidor:
        html = las(UT / s["fil"])
        for href in re.findall(r'(?:href|action)="([^"#?]*)', html):
            if not href or re.match(r"^(https?:|mailto:|tel:|/|#)", href):
                continue
            if href in finns or (UT / href).exists():
                continue
            saknade.add(href)
    if saknade:
        varningar.append(f"länkar till {len(saknade)} sidor som inte är byggda ännu: " + ", ".join(sorted(saknade)))

    print(f"\n{len(sidor)} sidor byggda till docs/  (STAGING={STAGING}, {SITE_URL})")
    for v in sorted(set(varningar)):
        print("VARNING:", v)
    for f in fel:
        print("FEL:", f)
    if fel:
        sys.exit(1)


if __name__ == "__main__":
    bygg()
