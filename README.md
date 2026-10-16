# avfallskonsulten.se, ny sajt

Statisk webbplats för Avfallskonsulten i huvudstaden AB. Koden ligger på GitHub
(VilleStrada/avfallskonsulten-web) och publiceras via GitHub Pages.

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
| `docs/` | **Den färdiga sajten.** Skapas av `build.py`, ändra aldrig här |
| `site-kopia/` | Komplett kopia av gamla sajten (alla 36 sidor + bilder), tagen 2026-10-16 |
| `build.py` | Byggskriptet |
| `Forhandsgranska.cmd` | Bygger och visar sajten lokalt i webbläsaren |
| `Publicera.cmd` | Bygger och skickar till GitHub, sajten uppdateras inom någon minut |

## Ändra text

1. Öppna rätt fil i `src/sidor/` (eller `src/mallar/` om texten finns på alla sidor, till exempel sidfoten).
2. Ändra texten. Längst upp i varje sida finns `titel` och `beskrivning`, det är vad Google visar.
3. Dubbelklicka på `Forhandsgranska.cmd` för att titta, sedan `Publicera.cmd` för att lägga ut.

Skriv kundtext utan tankstreck, använd komma. Byggskriptet varnar om det hittar tankstreck.

## Lägga till en sida

1. Kopiera `src/sidor/hamta-grovsopor-stockholm.html` till ett nytt filnamn, samma som adressen ska vara
   (till exempel `karltvatt.html` för `/karltvatt`). Gamla sajtens adresser ska behållas exakt.
2. Ändra `titel`, `beskrivning` och `og_bild` längst upp, och innehållet under.
3. Texten från gamla sidan finns i `site-kopia/<samma-namn>.html`.
4. Bilder: lägg originalet i `src/bilder/` och skriv `<x-bild src="filnamn-utan-ändelse" alt="beskrivning">` i sidan.
   Byggskriptet gör webp, srcset, width/height och lazy loading. Lägg till `eager` på bilden i hero.
5. Frågor och svar skrivs som `<details class="faq"><summary>Fråga</summary><p>Svar</p></details>`.
   Byggskriptet gör automatiskt FAQ-schema (JSON-LD) av dem.
6. Lägg in länk till sidan i `src/mallar/header.html` och/eller `footer.html` om den ska synas i menyn.
7. Sitemap.xml skapas automatiskt. Sidor som inte ska vara med får `sitemap: nej` längst upp.

## Publicera

Dubbelklicka på `Publicera.cmd`. Den kör `build.py`, stoppar om något är fel, och gör annars
`git add`, `git commit` och `git push`. GitHub Pages publicerar mappen `docs/` på grenen `main`.

Kräver att git och GitHub CLI är inloggade (`gh auth status`).

## Gå live (återstår)

I `build.py` finns `STAGING = True`. Så länge den är `True` får alla sidor `noindex,nofollow`,
robots.txt blockerar allt och canonical pekar på staging-adressen. Vid lansering:

1. Bygg klart resterande sidor (se listan som `build.py` varnar om).
2. Sätt `STAGING = False` i `build.py`, kör `Publicera.cmd`.
3. Koppla domänen: Cloudflare (DNS + 301-regler + formulär-backend) eller GitHub Pages custom domain.
4. Registrera sajten i Google Search Console och skicka in `sitemap.xml`.

## Bokningsformuläret

Formuläret har `action="#"` och skickas inte någonstans ännu. Det ska kopplas till en backend
som mejlar info@avfallskonsulten.se (planerat: Cloudflare Worker). Se kommentaren i
`src/mallar/boka.html` och `src/js/site.js`. Spamskydd finns redan i form av ett dolt fält (honungsfälla).

## Cookies och Google Analytics

GTM-id ligger i `build.py` (`GTM_ID`). Taggen laddas bara om besökaren klickar Acceptera i cookie-rutan.
Valet sparas i webbläsaren och kan ändras via Cookie-inställningar i sidfoten.
