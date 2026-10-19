"""Bygger en enkel områdeskarta (SVG) över Stockholm och Lidingö med grannkommuner i grått.
Kommungränser från OpenStreetMap via Nominatim (json-filerna i samma mapp, hämtade 2026-10-19).
Skriver src/mallar/karta.html som inlinas på om oss-sidan.
Kör: python tools/karta/bygg_karta.py
"""
import json, math
from pathlib import Path

H = Path(__file__).resolve().parent
UT = H.parents[1] / "src" / "mallar" / "karta.html"
FRAMHAVDA = ["Stockholms_kommun", "Lidingo_kommun"]
GRANNAR = ["Solna_kommun", "Sundbybergs_kommun", "Nacka_kommun", "Danderyds_kommun", "Huddinge_kommun",
           "Sollentuna_kommun", "Jarfalla_kommun", "Taby_kommun", "Tyreso_kommun", "Varmdo_kommun",
           "Ekero_kommun", "Botkyrka_kommun", "Haninge_kommun"]
NAMN = {"Stockholms_kommun": "Stockholm", "Lidingo_kommun": "Lidingö"}
W, Hh = 900, 760
LAT0 = 59.33

def ringar(gj):
    g = gj["geojson"]
    if g["type"] == "Polygon":
        return [g["coordinates"][0]]
    return [p[0] for p in g["coordinates"]]

def forenkla(pts, tol):
    """Douglas-Peucker."""
    if len(pts) < 3: return pts
    def avst(p, a, b):
        (x, y), (x1, y1), (x2, y2) = p, a, b
        dx, dy = x2 - x1, y2 - y1
        if dx == dy == 0: return math.hypot(x - x1, y - y1)
        t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
        return math.hypot(x - (x1 + t * dx), y - (y1 + t * dy))
    imax, dmax = 0, 0
    for i in range(1, len(pts) - 1):
        d = avst(pts[i], pts[0], pts[-1])
        if d > dmax: imax, dmax = i, d
    if dmax > tol:
        return forenkla(pts[:imax + 1], tol)[:-1] + forenkla(pts[imax:], tol)
    return [pts[0], pts[-1]]

data = {}
for namn in FRAMHAVDA + GRANNAR:
    gj = json.load(open(H / f"{namn}.json", encoding="utf-8"))[0]
    data[namn] = ringar(gj)

# projektion: enkel plattkarta skalad med cos(lat)
allt = [p for r in data["Stockholms_kommun"] + data["Lidingo_kommun"] for p in r]
lons = [p[0] for p in allt]; lats = [p[1] for p in allt]
# lite luft runt Stockholm + Lidingö
minlon, maxlon = min(lons) - 0.05, max(lons) + 0.08
minlat, maxlat = min(lats) - 0.03, max(lats) + 0.03
k = math.cos(math.radians(LAT0))
sx = W / ((maxlon - minlon) * k); sy = Hh / (maxlat - minlat)
s = min(sx, sy)
def proj(lon, lat):
    return ((lon - minlon) * k * s, (maxlat - lat) * s)

def path(rs, tol):
    d = []
    for r in rs:
        pts = [proj(*p) for p in r]
        pts = forenkla(pts, tol)
        if len(pts) < 3: continue
        d.append("M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts) + "Z")
    return " ".join(d)

ut = [f'<svg class="karta" viewBox="0 0 {W} {Hh}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="karta-titel">',
      '<title id="karta-titel">Karta över Stockholm och Lidingö, Avfallskonsultens hemmaplan</title>',
      '<g class="karta__grannar">']
for n in GRANNAR:
    ut.append(f'<path d="{path(data[n], 2.5)}"/>')
ut.append("</g>")
ut.append('<g class="karta__hemma">')
for n in FRAMHAVDA:
    ut.append(f'<path class="karta__{n.split("_")[0].lower()}" d="{path(data[n], 1.5)}"/>')
ut.append("</g>")
# etiketter
def mitt(rs):
    pts = [proj(*p) for r in rs for p in r]
    return sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts)
sx_, sy_ = mitt(data["Stockholms_kommun"]); lx, ly = mitt(data["Lidingo_kommun"])
ut.append(f'<text class="karta__etikett" x="{sx_:.0f}" y="{sy_ + 40:.0f}">Stockholm</text>')
ut.append(f'<text class="karta__etikett" x="{lx:.0f}" y="{ly - 18:.0f}">Lidingö</text>')
ut.append("</svg>")
svg = "\n".join(ut)
UT.write_text(svg + "\n", encoding="utf-8")
print(f"karta.html: {len(svg) // 1024} kB, Stockholm-centrum ca ({sx_:.0f},{sy_:.0f}), Lidingö ({lx:.0f},{ly:.0f})")
