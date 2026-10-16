"""Hämtar en komplett kopia av dagens avfallskonsulten.se till site-kopia/.
Sidor sparas som <slug>.html, tillgångar (bilder, css, js, pdf, typsnitt) under site-kopia/assets/.
Körs: python tools/hamta_kopia.py
"""
import re, os, sys, json, hashlib
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site-kopia")
BASE = "https://avfallskonsulten.se"
S = requests.Session()
S.headers["User-Agent"] = "Mozilla/5.0 (site backup for owner)"

def get(url):
    r = S.get(url, timeout=30, allow_redirects=True)
    return r

sitemap = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
print(len(urls), "sidor i sitemap")

assets = {}   # url -> local relative path
def local_asset(url):
    u = url.split("#")[0]
    if u in assets: return assets[u]
    p = urlparse(u)
    path = p.path.lstrip("/") or "index"
    if p.query:
        path += "_" + hashlib.md5(p.query.encode()).hexdigest()[:6]
    dest = os.path.join(ROOT, "assets", p.netloc, path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        r = get(u)
        ct = r.headers.get("content-type", "")
        if r.status_code == 200 and not ("text/html" in ct and not dest.endswith(".html")):
            open(dest, "wb").write(r.content)
            assets[u] = os.path.relpath(dest, ROOT).replace("\\", "/")
            # css: hämta refererade url(...)
            if dest.endswith(".css"):
                for m in re.findall(r"url\(['\"]?([^'\")]+)['\"]?\)", r.text):
                    if m.startswith("data:"): continue
                    local_asset(urljoin(u, m))
        else:
            assets[u] = None
            print("  MISS", r.status_code, ct.split(";")[0], u)
    except Exception as e:
        assets[u] = None
        print("  FEL", u, e)
    return assets[u]

report = []
for url in urls:
    r = get(url)
    slug = urlparse(url).path.strip("/") or "index"
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    n = 0
    for tag, attr in (("img","src"),("img","data-src"),("source","srcset"),("img","srcset"),("link","href"),("script","src"),("a","href"),("video","src"),("video","poster")):
        for el in soup.find_all(tag):
            v = el.get(attr)
            if not v: continue
            if tag == "link" and not any(x in (el.get("rel") or []) for x in ("stylesheet","icon","apple-touch-icon","shortcut")): continue
            if tag == "a" and not re.search(r"\.(pdf|jpe?g|png|svg|webp|docx?|xlsx?)(\?|$)", v, re.I): continue
            cands = [c.strip().split(" ")[0] for c in v.split(",")] if "srcset" in attr else [v]
            for c in cands:
                if not c or c.startswith("data:") or c.startswith("mailto:") or c.startswith("tel:"): continue
                full = urljoin(url, c)
                if urlparse(full).netloc not in ("avfallskonsulten.se","www.avfallskonsulten.se"): continue
                if local_asset(full): n += 1
    open(os.path.join(ROOT, slug + ".html"), "w", encoding="utf-8").write(html)
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    report.append({"url": url, "final_url": r.url, "status": r.status_code, "file": slug + ".html", "title": title, "bytes": len(r.content)})
    print(r.status_code, slug, "|", title, "|", n, "tillgångar")

json.dump({"pages": report, "assets": assets}, open(os.path.join(ROOT, "kopia-rapport.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ok = sum(1 for a in assets.values() if a)
print("Klart:", len(report), "sidor,", ok, "tillgångar sparade,", len(assets)-ok, "missade")
