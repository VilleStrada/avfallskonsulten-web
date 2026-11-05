# Lansering av nya avfallskonsulten.se

Checklista för bytet från gamla sajten till den nya på samma domän. Domänen är densamma, så Search Consoles
verktyg för adressbyte används inte. Det som skyddar rankningen är att varje gammal adress ger en sida eller en 301,
att titlar och beskrivningar på sidorna som rankar behålls, och att vi mäter före och efter.
Räkna med ett tillfälligt tapp i organisk trafik de första veckorna. Underlaget kommer från Vanna Vallien (Emax Media), november 2026.

## Underlag i repot

| Fil | Vad |
|---|---|
| `innehall/gamla-urler.csv` | Alla kända adresser på gamla sajten: sitemap.xml, en genomsökning av live-sajten 2026-11-05 och Wayback Machine (WordPress-adresser från 2018 till 2022). 54 sidor och filer, 308 bilder |
| `innehall/gamla-bilder.csv` | Gamla bildadresser och vilken ny bild de omdirigeras till (skapas av `tools/matcha_gamla_bilder.py`) |
| `tools/kolla_gamla_urler.py` | Jämför listan med nya sajten (sidor i `docs/` och 301:or i `src/.htaccess`). `--live` frågar den riktiga sajten |
| `site-kopia/` | HTML-kopia av gamla sajten 2026-10-16 (36 sidor, bilder som webp). Inte en filbackup |

Läget 2026-11-05: alla 53 gamla sidor och filer har en sida eller en 301 på nya sajten, testat i Apache 2.4 med
sajtens `.htaccess`. Varje omdirigering är ett hopp. Det enda som saknas är `/public/public.css` (gamla sajtens stilmall, inget att göra).
Av 308 gamla bildadresser får 276 en 301 till samma bild på nya sajten (matchade på filnamn eller bildinnehåll,
lista i `innehall/gamla-bilder.csv`). De 32 som inte går att matcha ger 410 (borttagen).

## Före lansering

- [ ] **Backup.** Ladda ner hela webbhotellets mapp via FTP, särskilt gamla `.htaccess`. Den innehåller omdirigeringarna
      som finns i dag. Jämför dem med avsnitt 3 i `src/.htaccess` och lägg till det som saknas.
- [ ] **Search Console, baslinje.** Exportera Resultat (sidor och sökfrågor, senaste 16 månaderna) och Indexering > Sidor.
      Lägg in adresser som inte finns i `innehall/gamla-urler.csv` och kör `python tools/kolla_gamla_urler.py`.
- [ ] **Search Console, åtkomst.** Kontrollera att Emax (teamemax@emaxmedia.se) har åtkomst till Search Console, GA4 och Tag Manager.
- [ ] **GA4, baslinje.** Notera organiska sessioner per landningssida och antal förfrågningar och samtal per vecka.
      GTM-id är detsamma på nya sajten (`GTM_ID` i `build.py`), men taggen laddas först efter cookie-samtycke.
- [ ] **Titlar och beskrivningar.** Behåll gamla titlar på sidorna som rankar. Ändrade i dag jämfört med gamla sajten:
      - Startsidan: `Avfallshantering Stockholm | 5/5 på Reco | Avfallskonsulten` blev `Avfallshantering i Stockholm och Lidingö | Avfallskonsulten`.
      - Grovsopor Stockholm: `Hämta grovsopor Stockholm | Grovavfall | Avfallskonsulten` fick tillägget `från 275 kr`.
      - Två titlar har bara fått komma i stället för bindestreck (sophämtning företag, fastighetsnära insamling 2027).
      - Nya beskrivningar på startsidan och grovsopor Stockholm, och på kontakt, om oss, produkter och projekt där gamla sajten saknade beskrivning.
      Stäm av startsidans titel med Vanna innan lansering.
- [ ] **Bygg för live.** `STAGING = False` i `build.py`, bygg, kontrollera att `noindex` är borta, att canonical pekar på
      `https://avfallskonsulten.se` och att `robots.txt` har `Allow` och sitemap-raden.

## Lanseringsdagen

- [ ] Ladda upp med `Publicera-Loopia.cmd`. Ta bort gamla sajtens filer som inte längre behövs, men behåll backupen.
- [ ] Kör `python tools/kolla_gamla_urler.py --live`. Alla rader ska vara OK. Kontrollen 2026-11-05 mot gamla sajten gav 19 fel
      (302 till startsidan och extra hopp), de ska vara borta.
- [ ] Kontrollera för hand: `http://www.avfallskonsulten.se/atervinning/` hamnar på `https://avfallskonsulten.se/atervinning-stockholm`,
      en påhittad adress ger 404-sidan med status 404, och en testförfrågan i formuläret kommer fram till info@.
- [ ] Search Console: skicka in `https://avfallskonsulten.se/sitemap.xml`, inspektera startsidan och de fem sidorna med
      flest klick och begär indexering.

## Efter lansering

- [ ] **Vecka 1.** Search Console > Indexering > Sidor varannan dag: nya 404:or får en 301 i avsnitt 3 i `src/.htaccess`.
      Titta på Genomsökningsstatistik efter fel.
- [ ] **Vecka 2 och 4.** Jämför klick, visningar och position per sida mot baslinjen. Ett tapp som går tillbaka inom några
      veckor är normalt. Sidor som tappar mer än övriga: jämför titel, beskrivning, rubriker och text mot `site-kopia/`.
- [ ] **Vecka 4 och 8.** Core Web Vitals i Search Console. Förfrågningar och samtal per vecka mot baslinjen i GA4.
- [ ] **Länkar utifrån.** Uppdatera adresser i Google Företagsprofil, Reco, Facebook, Instagram och kataloger om de pekar
      på gamla adresser (de fungerar via 301, men en direkt länk är bättre).
- [ ] **Intern länkning.** Nya landningssidor ska ha länkar från startsidan, menyn eller närliggande tjänstesidor.
