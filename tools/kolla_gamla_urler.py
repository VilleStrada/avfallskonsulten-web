"""Jämför alla gamla adresser i innehall/gamla-urler.csv med den nya sajten.

För varje gammal adress: finns sidan/filen i docs/, eller fångas den av en 301 i src/.htaccess?
Skriver kolumnerna ny_sajt och ny_adress i CSV-filen och listar det som saknas.
Kör efter build.py:  python tools/kolla_gamla_urler.py
Efter lansering:     python tools/kolla_gamla_urler.py --live
  (frågar den riktiga sajten om varje gammal sida och fil och visar antal hopp och slutstatus)
"""
import csv
import re
import sys
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
CSV = ROT / "innehall" / "gamla-urler.csv"
DOCS = ROT / "docs"


def regler():
    """RewriteRule med R=301 från avsnitt 3 i .htaccess (de som pekar på en fast adress)."""
    ut = []
    for rad in (ROT / "src" / ".htaccess").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*RewriteRule\s+(\S+)\s+(?:https://avfallskonsulten\.se)?(/\S*)\s+\[R=301", rad)
        if m and "%" not in m.group(2):
            ut.append((re.compile(m.group(1)), m.group(2)))
    return ut


def finns(adress):
    s = adress.strip("/")
    if not s:
        return (DOCS / "index.html").exists()
    return (DOCS / f"{s}.html").exists() or (DOCS / s).is_file()


def kolla(adress, regellista):
    """Returnerar (ny_sajt, ny_adress). Följer omdirigeringar som Apache gör: först 301-reglerna, sedan snedstreck bort."""
    sokvag = adress.split("?")[0]
    for _ in range(5):
        for monster, mal in regellista:
            m = monster.match(sokvag.lstrip("/"))
            if m:
                mal = m.expand(re.sub(r"\$(\d)", r"\\\1", mal))  # $1 i Apache blir \1 i Python
                if finns(mal):
                    return "301", mal
                sokvag = mal
                break
        else:
            if finns(sokvag):
                return ("sida finns" if sokvag == adress else "301"), ("" if sokvag == adress else sokvag)
            if sokvag.endswith("/") and finns(sokvag.rstrip("/")):
                return "301", sokvag.rstrip("/")
            return "SAKNAS (404)", ""
    return "SAKNAS (loop)", ""


def live_kontroll(rader, bas="https://avfallskonsulten.se"):
    import urllib.error
    import urllib.parse
    import urllib.request

    class IngenOmdirigering(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    op = urllib.request.build_opener(IngenOmdirigering)
    fel = 0
    for r in rader:
        if r["typ"] == "bild":
            continue
        url, hopp = bas + urllib.parse.quote(r["adress"]), []
        for _ in range(6):
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (kolla_gamla_urler)"})
            try:
                svar = op.open(req, timeout=20)
                hopp.append(svar.status)
                break
            except urllib.error.HTTPError as e:
                hopp.append(e.code)
                if e.code in (301, 302, 307, 308) and e.headers.get("Location"):
                    url = urllib.parse.urljoin(url, e.headers["Location"])
                    continue
                break
            except Exception as e:  # nätverksfel
                hopp.append(0)
                break
        slut = url.replace(bas, "") or "/"
        forvantat = r["adress"] if r["ny_sajt"] == "sida finns" else r["ny_adress"]
        ok = hopp[-1] == 200 and slut.rstrip("/") == (forvantat or "").rstrip("/") and 302 not in hopp and len(hopp) <= 2
        if not ok and not r["ny_sajt"].startswith("SAKNAS"):
            fel += 1
        print(f"  {'OK ' if ok else 'FEL'} {r['adress']:52s} {'>'.join(map(str, hopp)):10s} {slut}")
    print(f"\n{fel} fel (sidor som inte hamnar rätt, går via 302 eller kräver fler än ett hopp)")
    return 1 if fel else 0


def main():
    rader = list(csv.DictReader(CSV.open(encoding="utf-8")))
    falt = [f for f in rader[0].keys() if f not in ("ny_sajt", "ny_adress")] + ["ny_sajt", "ny_adress"]
    rl = regler()
    saknas = []
    for r in rader:
        r["ny_sajt"], r["ny_adress"] = kolla(r["adress"], rl)
        if r["ny_sajt"].startswith("SAKNAS"):
            saknas.append(r)
    with CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=falt)
        w.writeheader()
        w.writerows(rader)
    sidor = [r for r in rader if r["typ"] != "bild"]
    print(f"{len(rader)} gamla adresser, varav {len(sidor)} sidor och filer.")
    for r in sidor:
        print(f"  {r['adress']:52s} gamla: {r['status_gamla_sajten']:3s} {r['gamla_sajten_skickar_till']:32s} ny: {r['ny_sajt']} {r['ny_adress']}")
    bilder = [r for r in saknas if r["typ"] == "bild"]
    print(f"\nSaknas på nya sajten: {len(saknas) - len(bilder)} sidor/filer och {len(bilder)} bilder (gamla /images/, nya bilder ligger i /bilder/).")
    for r in saknas:
        if r["typ"] != "bild":
            print("  SAKNAS:", r["adress"])
    if "--live" in sys.argv:
        print("\nKontroll mot den riktiga sajten:")
        return live_kontroll(rader)
    return 0


if __name__ == "__main__":
    sys.exit(main())
