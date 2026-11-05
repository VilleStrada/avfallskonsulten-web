"""Matchar gamla bildadresser (innehall/gamla-urler.csv) mot nya bilder: först filnamn, sedan innehåll (dHash)
mot bilderna i src/bilder, med gamla bilderna från site-kopia/. Skriver innehall/gamla-bilder.csv och avsnittet
med bildomdirigeringar i src/.htaccess mellan markeringarna. Kör efter build.py:
  python tools/matcha_gamla_bilder.py
"""
import csv, json, os, re, sys
from PIL import Image
ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = [r for r in csv.DictReader(open(f'{ROT}/innehall/gamla-urler.csv', encoding='utf-8')) if r['typ'] == 'bild']
assets = json.load(open(f'{ROT}/site-kopia/kopia-rapport.json'))['assets']
lokal = {re.sub(r'^https?://(www\.)?avfallskonsulten\.se', '', u): p for u, p in assets.items()}
byggda = {}
for f in os.listdir(f'{ROT}/docs/bilder'):
    m = re.match(r'(.+)-(\d+)\.webp$', f)
    if m: byggda.setdefault(m.group(1), []).append(int(m.group(2)))
def dhash(path):
    try:
        im = Image.open(path).convert('L').resize((17, 16), Image.LANCZOS)
    except Exception:
        return None
    px = list(im.getdata() if not hasattr(im, "get_flattened_data") else im.get_flattened_data()); bits = 0
    for y in range(16):
        for x in range(16):
            bits = bits << 1 | (px[y*17+x] > px[y*17+x+1])
    return bits
nya = {}
for f in os.listdir(f'{ROT}/src/bilder'):
    s, e = os.path.splitext(f)
    if s in byggda and e.lower() in ('.jpg', '.jpeg', '.png', '.webp'):
        h = dhash(f'{ROT}/src/bilder/{f}')
        if h is not None: nya[s] = h
def stam(p):
    n = p.rsplit('/', 1)[-1]
    return re.sub(r'(\.(jpe?g|png|webp|gif|svg|jfif|jeg|jpgp))+$', '', n, flags=re.I)
ut = []
for r in rows:
    p = r['adress']; s = stam(p); mal = metod = ''
    if s in byggda:
        mal, metod = s, 'namn'
    else:
        kand = lokal.get(p) or lokal.get(re.sub(r'\.(jpe?g)$', '.webp', p))
        if not kand:  # samma bild finns ofta som .webp i kopian
            for alt in (re.sub(r'(\.\w+)+$', '.webp', p), re.sub(r'(\.\w+)+$', '.jpg', p)):
                if alt in lokal: kand = lokal[alt]; break
        h = dhash(f'{ROT}/site-kopia/{kand}') if kand else None
        if h is not None:
            bast = min(nya, key=lambda n: bin(nya[n] ^ h).count('1'))
            d = bin(nya[bast] ^ h).count('1')
            if d <= 10: mal, metod = bast, f'innehåll (avstånd {d})'
            else: metod = f'ingen match (närmast {bast}, avstånd {d})'
        else:
            metod = 'ingen kopia av bilden'
    ut.append({'adress': p, 'kallor': r['kallor'], 'ny_bild': (f"/bilder/{mal}-{max(byggda[mal])}.webp" if mal else ''), 'metod': metod})
# filer som ligger kvar på samma eller ny plats på nya sajten
for x in ut:
    if not x['ny_bild'] and x['adress'] == '/logga.svg':
        x['ny_bild'], x['metod'] = '/bilder/logga.svg', 'namn'
    if not x['ny_bild'] and os.path.isfile(ROT + '/docs' + x['adress']):
        x['ny_bild'], x['metod'] = x['adress'], 'finns kvar'
with open(f'{ROT}/innehall/gamla-bilder.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=['adress', 'ny_bild', 'metod', 'kallor']); w.writeheader(); w.writerows(ut)
START, SLUT = '# BILDER START (skapas av tools/matcha_gamla_bilder.py, ändra inte för hand)', '# BILDER SLUT'
rader = [START, '# Gamla bildadresser från förra sajten -> samma bild på nya sajten. Övriga under /images/ ger 410 (borttagen).']
for x in ut:
    if x['ny_bild'] and x['ny_bild'] != x['adress']:
        rader.append(f"RewriteRule ^{re.escape(x['adress'].lstrip('/'))}$ https://avfallskonsulten.se{x['ny_bild']} [R=301,L]")
rader += ['RewriteRule ^images/ - [G,L]', SLUT]
ht = open(f'{ROT}/src/.htaccess', encoding='utf-8').read()
if START in ht:
    ht = ht[:ht.index(START)] + '\n'.join(rader) + ht[ht.index(SLUT) + len(SLUT):]
else:
    mark = '\n# 4. index.html'
    ht = ht.replace(mark, '\n' + '\n'.join(rader) + '\n' + mark, 1)
open(f'{ROT}/src/.htaccess', 'w', encoding='utf-8').write(ht)
from collections import Counter
print(Counter(x['metod'].split(' (')[0] for x in ut), 'regler:', len(rader) - 4)
