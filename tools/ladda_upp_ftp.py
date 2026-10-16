"""Laddar upp docs/ till Loopia-webbhotellet via FTP (med TLS om servern stödjer det).

Uppgifterna läses från .env i repots rot (filen är gitignorad):
    FTP_HOST=ftpcluster.loopia.se
    FTP_USER=användarnamn@avfallskonsulten.se
    FTP_PASS=lösenord
    FTP_MAPP=/avfallskonsulten.se/public_html      (mappen på servern som är sajtens rot)

Kör:  python tools/ladda_upp_ftp.py            laddar upp alla filer
      python tools/ladda_upp_ftp.py --torr      visar bara vad som skulle laddas upp
Filer tas aldrig bort på servern, bara skapas/ersätts.
"""
import ftplib
import os
import sys
from pathlib import Path

ROT = Path(__file__).resolve().parents[1]
DOCS = ROT / "docs"
TORR = "--torr" in sys.argv


def las_env():
    env = {}
    p = ROT / ".env"
    if not p.exists():
        sys.exit("Hittar ingen .env i " + str(ROT) + ". Kopiera .env.exempel till .env och fyll i FTP-uppgifterna.")
    for rad in p.read_text(encoding="utf-8").splitlines():
        rad = rad.strip()
        if rad and not rad.startswith("#") and "=" in rad:
            k, v = rad.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("FTP_HOST", "FTP_USER", "FTP_PASS", "FTP_MAPP"):
        if not env.get(k):
            sys.exit(f"{k} saknas i .env")
    return env


def anslut(env):
    try:
        ftp = ftplib.FTP_TLS(env["FTP_HOST"], timeout=60)
        ftp.login(env["FTP_USER"], env["FTP_PASS"])
        ftp.prot_p()
        print("Ansluten med FTP + TLS")
    except Exception as e:
        print("TLS gick inte (", e, "), provar vanlig FTP")
        ftp = ftplib.FTP(env["FTP_HOST"], timeout=60)
        ftp.login(env["FTP_USER"], env["FTP_PASS"])
    ftp.encoding = "utf-8"
    return ftp


def se_till_att_mapp_finns(ftp, mapp, cache):
    if mapp in cache or mapp in ("", "/"):
        return
    se_till_att_mapp_finns(ftp, os.path.dirname(mapp.rstrip("/")), cache)
    try:
        ftp.mkd(mapp)
    except ftplib.error_perm:
        pass
    cache.add(mapp)


def main():
    env = las_env()
    if not DOCS.exists():
        sys.exit("docs/ saknas, kör build.py först")
    filer = [p for p in DOCS.rglob("*") if p.is_file()]
    print(f"{len(filer)} filer i docs/, mål: {env['FTP_HOST']}{env['FTP_MAPP']}")
    if TORR:
        for p in filer:
            print("  skulle ladda upp", p.relative_to(DOCS).as_posix())
        return
    ftp = anslut(env)
    bas = env["FTP_MAPP"].rstrip("/")
    mappar = set()
    for i, p in enumerate(filer, 1):
        rel = p.relative_to(DOCS).as_posix()
        fjarr = f"{bas}/{rel}"
        se_till_att_mapp_finns(ftp, os.path.dirname(fjarr), mappar)
        with open(p, "rb") as f:
            ftp.storbinary("STOR " + fjarr, f)
        print(f"  [{i}/{len(filer)}] {rel}")
    ftp.quit()
    print("Klart. Kontrollera https://avfallskonsulten.se/ i webbläsaren.")


if __name__ == "__main__":
    main()
