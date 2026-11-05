"""Jämför alla gamla adresser i innehall/gamla-urler.csv med den nya sajten.

För varje gammal adress: finns sidan/filen i docs/, eller fångas den av en 301 i src/.htaccess?
Skriver kolumnerna ny_sajt och ny_adress i CSV-filen och listar det som saknas.
Kör efter build.py:  python tools/kolla_gamla_urler.py
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
