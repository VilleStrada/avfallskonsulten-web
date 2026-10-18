"""Gör om textexporten i innehall/sidor/<slug>.md till sidor i src/sidor/<slug>.html i sajtens mall.

Kör:  python tools/md_till_sida.py            (hoppar över sidor som redan finns i src/sidor/)
      python tools/md_till_sida.py --skriv-over hamta-grovsopor-taby   (skriver över en viss sida)

Det som görs per sida:
- title, description och H1 tas ur exporten
- första bilden blir hero-bild, första stycket ingress, första knappen hero-knapp
- bilder kopieras till src/bilder/ (trasiga ersätts med webp ur site-kopia/) och blir <x-bild>
- "Vanliga frågor"-listor blir <details class="faq"> (ger FAQ-schema automatiskt)
- "Vad våra kunder säger om oss" blir Reco-widgeten
- avslutande "Frågor?"/"KONTAKTA OSS" tas bort, bokningsformuläret läggs in i stället
- länkar till #kontakt-form och kontakt blir #offert, tankstreck blir komma, platshållaren "område" fylls i
"""
import re
import shutil
import sys
from pathlib import Path

import markdown
from PIL import Image

ROT = Path(__file__).resolve().parents[1]
EXPORT = ROT / "innehall"
KOPIA_BILDER = ROT / "site-kopia" / "assets" / "avfallskonsulten.se" / "images"
UT = ROT / "src" / "sidor"
BILDER = ROT / "src" / "bilder"
SKRIV_OVER = "--skriv-over" in sys.argv
BARA = [a for a in sys.argv[1:] if not a.startswith("--")]

KOMMUN = {"jarfalla": "Järfälla", "lidingo": "Lidingö", "norrtalje": "Norrtälje", "sollentuna": "Sollentuna",
          "sundbyberg": "Sundbyberg", "taby": "Täby", "stockholm": "Stockholm"}
HOPPA_OVER = {"startsida", "hamta-grovsopor-stockholm"}  # redan byggda för hand


def slugify(t):
    import html as _html
    t = _html.unescape(t).lower()
    for a, b in (("å", "a"), ("ä", "a"), ("ö", "o"), ("&", "och"), ("é", "e")):
        t = t.replace(a, b)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t


def knapptext(t):
    t = t.strip()
    return t[:1].upper() + t[1:].lower() if t.isupper() else t


def ar_bild_ok(p):
    try:
        if p.stat().st_size == 76164:
            return False
        Image.open(p).verify()
        return True
    except Exception:
        return False


def hamta_bild(ref):
    """'../bilder/namn_hash.ext' -> stem i src/bilder (kopierar vid behov), eller None."""
    namn = Path(ref).name
    stem = re.sub(r"_[0-9a-f]{6}$", "", Path(namn).stem)
    if stem in ("logga",):
        return None
    for p in BILDER.iterdir():
        if p.stem == stem and p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            return stem
    kalla = EXPORT / "bilder" / namn
    if not (kalla.exists() and ar_bild_ok(kalla)):
        kand = [q for q in KOPIA_BILDER.iterdir() if q.stem == stem and q.suffix.lower() == ".webp" and ar_bild_ok(q)]
        kand += [q for q in KOPIA_BILDER.iterdir() if q.stem == stem and q.suffix.lower() in (".jpg", ".jpeg", ".png") and ar_bild_ok(q)]
        if not kand:
            print(f"    bild saknas/trasig, hoppas över: {namn}")
            return None
        kalla = kand[0]
    mal = BILDER / (stem + kalla.suffix.lower().replace(".jpeg", ".jpg"))
    shutil.copy(kalla, mal)
    return stem


def fixa_lankar(t, slug):
    t = t.replace("#kontakt-form", "#offert")
    t = re.sub(r"\]\(kontakt\)", "](#offert)", t)
    t = t.replace("tel:08-68427888", "tel:+46868427888")
    t = re.sub(r"\]\(https?://(?:www\.)?avfallskonsulten\.se/?([^)]*)\)", lambda m: "](" + (m.group(1) or "./") + ")", t)
    t = t.replace("](/)", "](./)")
    t = re.sub(r"\]\(/([a-z0-9_\-]+)\)", r"]()", t)  # /sida -> sida (relativt, fungerar även under /avfallskonsulten-web/)
    t = re.sub(r"\*\*-\s*", "**", t)  # exportens "**-Källsortering**" -> "**Källsortering**"
    t = re.sub(r"^(\s*[-*] )\*\*-\*\* ", r"", t, flags=re.M)  # "- **-** Papper" -> "- Papper"
    t = t.replace("Info@avfallskonsulten.se", "info@avfallskonsulten.se")
    return t


def fixa_text(t, slug):
    kommun = KOMMUN.get(slug.replace("hamta-grovsopor-", ""), "") if slug.startswith("hamta-grovsopor-") else ""
    ers = f" i {kommun}" if kommun else ""
    t = re.sub(r"(grovsopor|grovavfall|skräp|företag) område\b", lambda m: m.group(1) + ers, t)
    t = t.replace(" – ", ", ").replace("–", "-").replace("—", ", ")
    return t


def konvertera(mdfil):
    slug = mdfil.stem
    if slug == "startsida":
        slug = "index"
    text = mdfil.read_text(encoding="utf-8")
    huvud, _, body = text.partition("\n---\n")
    meta = {}
    for m in re.finditer(r"- \*\*(.+?):\*\* ?(.*)", huvud):
        meta[m.group(1)] = m.group(2).strip()
    titel = meta.get("Title-tagg") or ""
    beskrivning = meta.get("Meta description") or ""

    body = fixa_lankar(fixa_text(body.strip(), slug), slug)
    titel = fixa_text(titel, slug)
    beskrivning = fixa_text(beskrivning, slug)

    # klipp bort avslutande "Frågor?" / "KONTAKTA OSS"
    body = re.split(r"\n## Frågor\?\s*\n", body)[0]
    body = re.split(r"\n### KONTAKTA OSS\s*\n", body)[0].rstrip()

    rader = body.split("\n")
    platshallare = {}

    def ph(html):
        k = f"PLATSHALLARE{len(platshallare)}X"
        platshallare[k] = html
        return k

    # hero: första bild, H1, första stycke, första knapp
    hero_bild = None
    h1 = None
    ingress = None
    hero_knapp = None
    ut = []
    i = 0
    while i < len(rader):
        r = rader[i]
        mb = re.match(r"!\[(.*?)\]\((.+?)\)\s*$", r.strip())
        if mb and hero_bild is None and h1 is None:
            hero_bild = (hamta_bild(mb.group(2)), mb.group(1)); i += 1; continue
        if r.startswith("# ") and h1 is None:
            h1 = r[2:].strip()
            i += 1
            # ingress = nästa icke-tomma stycke om det är text
            while i < len(rader) and not rader[i].strip():
                i += 1
            if i < len(rader) and not rader[i].startswith(("#", "!", "[", "- ", "* ", "1")) and len(rader[i]) < 650:
                ingress = rader[i].strip(); i += 1
            while i < len(rader) and not rader[i].strip():
                i += 1
            mk = re.match(r"\[([^\]]+)\]\(([^)]+)\)\s*$", rader[i].strip()) if i < len(rader) else None
            if mk and (mk.group(1).isupper() or mk.group(1).split()[0].isupper()):
                hero_knapp = (knapptext(mk.group(1)), mk.group(2)); i += 1
            continue
        ut.append(r); i += 1
    rader = ut
    if not h1:
        h1 = huvud.splitlines()[0].lstrip("# ").strip()
    if not titel:
        titel = h1 + " | Avfallskonsulten"
    if not beskrivning:
        beskrivning = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", ingress or h1)[:155]
    if not hero_bild or not hero_bild[0]:
        hero_bild = ("hero_lastbil", "Avfallskonsultens lastbil i Stockholm")

    # FAQ-block -> details
    ut = []
    i = 0
    while i < len(rader):
        r = rader[i]
        if r.startswith("## Vanliga frågor"):
            rubrik = r[3:].strip()
            fragor = []
            i += 1
            while i < len(rader) and not rader[i].startswith("## "):
                mq = re.match(r"\s*\d+\.\s+###\s*(.+)", rader[i])
                if mq:
                    q = mq.group(1).strip()
                    svar = []
                    i += 1
                    while i < len(rader) and not re.match(r"\s*\d+\.\s+###", rader[i]) and not rader[i].startswith("## "):
                        s = re.sub(r"^\s*-\s+", "", rader[i]).strip()
                        if s:
                            svar.append(s)
                        i += 1
                    fragor.append((q, " ".join(svar)))
                else:
                    i += 1
            html = [f"<h2>{inline(rubrik)}</h2>", '<div class="faq-lista">']
            for q, a in fragor:
                html.append(f'<details class="faq"><summary>{inline(q)}</summary>\n  <p>{inline(a)}</p></details>')
            html.append("</div>")
            ut.append(ph("\n".join(html)))
            continue
        ut.append(r); i += 1
    rader = ut

    # Reco, bilder, knappar
    ut = []
    for r in rader:
        s = r.strip()
        if s == "## Vad våra kunder säger om oss":
            ut.append(ph('<div class="reco reco--sida"><h2>Vad våra kunder säger om oss</h2>'
                         '<iframe class="reco__ram" src="https://widget.reco.se/v2/widget/4044118?mode=HORIZONTAL_QUOTE&amp;inverted=false&amp;border=true" '
                         'title="Kundomdömen om Avfallskonsulten på Reco" loading="lazy" width="100%" height="225" frameborder="0" scrolling="no"></iframe></div>'))
            continue
        mb = re.match(r"!\[(.*?)\]\((.+?)\)$", s)
        if mb:
            stem = hamta_bild(mb.group(2))
            if stem:
                ut.append(ph(f'<x-bild src="{stem}" alt="{mb.group(1).replace(chr(34), "")}" sizes="(min-width: 900px) 820px, 100vw" klass="figur">'))
            continue
        mk = re.match(r"\[([^\]]+)\]\(([^)]+)\)$", s)
        if mk and (mk.group(1).isupper() or mk.group(1).split()[0].isupper()):
            ut.append(ph(f'<p class="knappar"><a class="knapp" href="{mk.group(2)}">{knapptext(mk.group(1))}</a></p>'))
            continue
        ut.append(r)
    body = "\n".join(ut)

    html = markdown.markdown(body, extensions=["sane_lists"])
    # platshållare tillbaka (markdown kan ha slagit in dem i <p>)
    for k, v in platshallare.items():
        html = html.replace(f"<p>{k}</p>", v).replace(k, v)
    # gallerier: två eller fler bilder i rad
    html = re.sub(r'((?:<x-bild [^>]*klass="figur">\s*){2,})',
                  lambda m: '<div class="galleri">' + m.group(1) + "</div>", html)
    # id på h2/h3 så att menyns ankare (produkter#sopkarl) fungerar
    html = re.sub(r"<(h[23])>(.*?)</\1>", lambda m: f'<{m.group(1)} id="{slugify(re.sub("<[^>]+>", "", m.group(2)))}">{m.group(2)}</{m.group(1)}>', html)
    html = html.replace("<h1>", "<h2>").replace("</h1>", "</h2>")  # bara en h1 per sida

    knapp_text, knapp_href = hero_knapp or ("Begär offert", "#offert")
    if knapp_href not in ("#offert",) and not knapp_href.startswith("#"):
        knapp_href = "#offert"
    sida = f"""---
titel: {titel}
beskrivning: {beskrivning}
og_bild: {hero_bild[0]}
body_klass: textsida
---
<section class="hero2 hero2--sida">
  <div class="hero2__media">
    <x-bild src="{hero_bild[0]}" alt="{hero_bild[1].replace(chr(34), '')}" sizes="100vw" eager>
  </div>
  <div class="wrap hero2__inner">
    <h1>{inline(h1)}</h1>
{('    <p class="hero2__ingress">' + inline(ingress) + '</p>') if ingress else ''}
    <div class="knappar">
      <a class="knapp knapp--stor" href="{knapp_href}">{knapp_text}</a>
      <a class="knapp knapp--ljus knapp--stor" href="tel:+46868427888">Ring 08-684 278 88</a>
    </div>
  </div>
</section>

{{{{include fortroende.html}}}}

<section class="sektion sektion--smal">
  <div class="wrap artikel">
{html}
  </div>
</section>

{{{{include boka.html}}}}
"""
    return slug, sida


def inline(t):
    """Markdown-inline (länkar, fetstil) -> HTML utan omslutande <p>."""
    h = markdown.markdown(t)
    return re.sub(r"^<p>(.*)</p>$", r"\1", h.strip(), flags=re.S)


def main():
    filer = sorted((EXPORT / "sidor").glob("*.md"))
    n = 0
    for f in filer:
        if f.stem in HOPPA_OVER:
            continue
        if BARA and f.stem not in BARA:
            continue
        slug, sida = konvertera(f)
        mal = UT / f"{slug}.html"
        if mal.exists() and not SKRIV_OVER:
            print(f"  finns redan, hoppar över: {mal.name}")
            continue
        mal.write_text(sida, encoding="utf-8")
        print(f"  skrev {mal.name}")
        n += 1
    print(f"{n} sidor skrivna till src/sidor/")


if __name__ == "__main__":
    main()
