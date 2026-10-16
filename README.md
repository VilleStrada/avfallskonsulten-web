# avfallskonsulten.se, ny sajt

Statisk webbplats för Avfallskonsulten i huvudstaden AB. Koden ligger på GitHub
(VilleStrada/avfallskonsulten-web). Förhandsvisning (staging) publiceras via GitHub Pages,
den riktiga sajten laddas upp via FTP till Villes Loopia-webbhotell där avfallskonsulten.se redan ligger.

**Staging (spärrad för Google):** https://villestrada.github.io/avfallskonsulten-web/

## Mappar

| Mapp / fil | Vad |
|---|---|
| `src/sidor/` | En fil per sida. Filnamnet blir adressen: `hamta-grovsopor-stockholm.html` → `/hamta-grovsopor-stockholm` |
| `src/mallar/` | Delar som återanvänds på alla sidor: `bas.html` (sidskalet), `header.html` (meny), `footer.html`, `cookie.html`, `boka.html` (bokningsformulär), `fortroende.html` (raden under hero) |
| `src/css/style.css` | All stil. Färger ligger överst som variabler |
| `src/js/site.js` | Meny, cookie-samtycke och formulär |
| `src/bilder/` | Originalbilder. Byggskriptet gör webp i flera storlekar |
| `src/typsnitt/` | Roboto, självhostad |
| `src/.htaccess` | Apache-regler för Loopia: 301-omdirigeringar, 404-sida, säkerhetsheaders, cache |
| `src/includes/skicka.php` | Tar emot bokningsformuläret och mejlar info@avfallskonsulten.se (körs bara på Loopia) |
| `docs/` | **Den färdiga sajten.** Skapas av `build.py`, ändra aldrig här |
| `site-kopia/` | Komplett kopia av gamla sajten (alla 36 sidor + bilder), tagen 2026-10-16 |
| `build.py` | Byggskriptet |
| `Forhandsgranska.cmd` | Bygger och visar sajten lokalt i webbläsaren |
| `Publicera.cmd` | Bygger och skickar till GitHub, staging uppdateras inom någon minut |
| `Publicera-Loopia.cmd` | Bygger och laddar upp till Loopia via FTP (den riktiga sajten) |
| `.env.exempel` | Mall för FTP-uppgifterna. Kopiera till `.env` och fyll i, `.env` hamnar aldrig på GitHub |

## Ändra text

1. Öppna rätt fil i `src/sidor/` (eller `src/mallar/` om texten finns på alla sidor, till exempel sidfoten).
2. Ändra texten. Längst upp i varje sida finns `titel` och `beskrivning`, det är vad Google visar.
3. Dubbelklicka på `Forhandsgranska.cmd` för att titta, sedan `Publicera.cmd` för att lägga ut på staging.

Skriv kundtext utan tankstreck, använd komma. Byggskriptet varnar om det hittar tankstreck.

## Lägga till en sida

1. Kopiera `src/sidor/hamta-grovsopor-stockholm.html` till ett nytt filnamn, samma som adressen ska vara
   (till exempel `karltvatt.html` för `/karltvatt`). Gamla sajtens adresser ska behållas exakt.
   Undantag: `/atervinning` och `/atervinning_brf` ska inte byggas, de omdirigeras i `.htaccess`
   till `/atervinning-stockholm` respektive `/atervinning_fastighet_och_brf`.
2. Ändra `titel`, `beskrivning` och `og_bild` längst upp, och innehållet under.
3. Texten från gamla sidan finns i `site-kopia/<samma-namn>.html`.
4. Bilder: lägg originalet i `src/bilder/` och skriv `<x-bild src="filnamn-utan-ändelse" alt="beskrivning">` i sidan.
   Byggskriptet gör webp, srcset, width/height och lazy loading. Lägg till `eager` på bilden i hero.
5. Frågor och svar skrivs som `<details class="faq"><summary>Fråga</summary><p>Svar</p></details>`.
   Byggskriptet gör automatiskt FAQ-schema (JSON-LD) av dem.
6. Lägg in länk till sidan i `src/mallar/header.html` och/eller `footer.html` om den ska synas i menyn.
7. Sitemap.xml skapas automatiskt. Sidor som inte ska vara med får `sitemap: nej` längst upp.

## Publicera till staging (GitHub Pages)

Dubbelklicka på `Publicera.cmd`. Den kör `build.py`, stoppar om något är fel, och gör annars
`git add`, `git commit` och `git push`. GitHub Pages publicerar mappen `docs/` på grenen `main`.
Kräver att git och GitHub CLI är inloggade (`gh auth status`).

## Publicera till Loopia (den riktiga sajten)

1. Kopiera `.env.exempel` till `.env` och fyll i FTP-uppgifterna från Loopia kundzon
   (FTP_HOST, FTP_USER, FTP_PASS och FTP_MAPP, mappen som är sajtens rot, oftast `/avfallskonsulten.se/public_html`).
2. Sätt `STAGING = False` i `build.py`. Då försvinner noindex, robots.txt öppnas och canonical pekar på https://avfallskonsulten.se.
   `Publicera-Loopia.cmd` vägrar köra om `STAGING` fortfarande är `True`.
3. Dubbelklicka på `Publicera-Loopia.cmd`. Den bygger, laddar upp hela `docs/` via FTP (TLS om servern stödjer det)
   och sparar ändringen på GitHub. Filer tas aldrig bort på servern, bara skapas eller ersätts.
   Första gången: ta bort gamla sajtens filer på webbhotellet, eller ladda upp till en testmapp först.
4. Ingen DNS-ändring behövs, domänen pekar redan på webbhotellet.

Efter första uppladdningen: kontrollera i webbläsaren att `http://www.avfallskonsulten.se/atervinning/`
hamnar på `https://avfallskonsulten.se/atervinning-stockholm`, att en påhittad adress ger 404-sidan,
och att formuläret kommer fram till info@. Registrera sedan sajten i Google Search Console och skicka in
`https://avfallskonsulten.se/sitemap.xml`.

## .htaccess

`src/.htaccess` kopieras till `docs/.htaccess` vid bygge. Den gör på Loopia:
http och www → `https://avfallskonsulten.se` i ett steg, avslutande snedstreck bort, `.html` bort ur adresser,
`/atervinning` → `/atervinning-stockholm`, `/atervinning_brf` → `/atervinning_fastighet_och_brf`,
`ErrorDocument 404 /404.html`, HSTS och andra säkerhetsheaders, cache för bilder/typsnitt, gzip.
GitHub Pages ignorerar filen. Lägg nya omdirigeringar under rubrik 3 i filen.

## Bokningsformuläret

Formuläret postar till `includes/skicka.php`, som kontrollerar fälten, stoppar robotar
(dolt fält "webbplats" och svar snabbare än 3 sekunder) och mejlar till info@avfallskonsulten.se
med kundens adress som Reply-To. Lyckad sändning skickar vidare till `/tack`, fel skickar tillbaka
till formuläret med ett felmeddelande. Avsändare är `noreply@avfallskonsulten.se` (ändra i filen
om Loopia kräver annan adress).

På staging finns ingen PHP, därför visar `site.js` bara tack-rutan där (styrs av `STAGING` i `build.py`).
Lokalt test med PHP installerat: `php -S localhost:8765 -t docs tools/php_router.php`, då sparas mejlen
som textfiler i `docs/includes/utkorg/` i stället för att skickas. Samma sak händer om filen
`includes/testlage.txt` finns på servern, så den får inte ligga kvar på Loopia.

## Cookies och Google Analytics

GTM-id ligger i `build.py` (`GTM_ID`). Taggen laddas bara om besökaren klickar Acceptera i cookie-rutan.
Valet sparas i webbläsaren och kan ändras via Cookie-inställningar i sidfoten.

## Återstår innan lansering

- Bygg resterande sidor (byggskriptet listar vilka länkmål som saknas, bland annat `/kontakt`).
- Ta bort prototyp-notisen i `src/sidor/404.html` och staging-notisen i `src/mallar/boka.html`.
- Läs igenom `src/sidor/integritetspolicy.html`, den är ett utkast.
- FTP-uppgifter i `.env`, `STAGING = False`, `Publicera-Loopia.cmd`, Search Console.
