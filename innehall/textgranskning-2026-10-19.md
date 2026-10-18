# Textgranskning av de 35 nya sidorna

Granskat 2026-10-19 utifrån texterna i `innehall/sidor/`. Inget är ändrat ännu. Sidorna har gamla sajtens texter rakt av, i ny design.

## 1. Det viktigaste, gäller många sidor

1. **Nya fokuset syns inte på tjänstesidorna.** Startsidan säljer nu hämtning av återvinning till brf i Stockholm och Lidingö med FNI 2027 som krok, men `/atervinning-stockholm`, `/atervinning_fastighet_och_brf` och `/fastighetsnara-insamling` nämner inte varandra, nämner inte Lidingö, och de två första nämner inte 2027 alls. Förslag: en tydlig "FNI 2027"-ruta med länk på båda återvinningssidorna, Lidingö i rubriker och text, och en offert-CTA i stället för "Kontakta oss".
2. **Sex nästan identiska kommunsidor för grovsopor** (Sundbyberg, Järfälla, Täby, Lidingö, Sollentuna, Norrtälje) skiljer sig bara i kommunnamnet. Google kan betrakta det som dörrmattesidor. Behåll adresserna, men ge varje sida minst ett eget stycke (vad som gäller i kommunen, återvinningscentral, typiska kunder, ett kundcitat) eller korta ner dem till en kortare lokal sida som länkar till huvudsidan. Lidingö-sidan bör dessutom lyftas till en riktig sida om återvinning på Lidingö, inte bara grovsopor, eftersom Lidingö nu är hemmaplan.
3. **Tre sidor säger samma sak om samma tjänst:** `/bortforsling`, `/hamta-skrap-stockholm` och `/tomma-dodsbo` har kopierade stycken och samma FAQ. Likaså `/atervinningsforetag-stockholm`, `/atervinning_for_foretag_och_verksamheter` och `/sophamtning-stockholm-foretag`. Förslag: en huvudsida per tjänst med fullt innehåll, de andra kortas till tydliga undersidor med eget syfte (dödsbo: känsligt läge, vad som ingår, pris; skräp: snabb engångshämtning).
4. **Löften som behöver bekräftas av dig** innan de får ligga kvar: "samma dag eller inom 24 timmar" (bortforsling, dödsbo), "container inom 24 timmar", "transport ingår i priset" (container), "100 % fossilfria transporter" (om oss), "låsta transportfordon" och "certifierade metoder" (sekretess), "rätt tillstånd för farligt avfall" (restaurang, företag), "dagliga hämtningar" (restaurang, företag), "vi hjälper till med kommunens tillstånd för container på allmän mark".
5. **Hushållens restavfall och matavfall.** `/hamtning-av-restavfall-stockholm` erbjuder hämtning av "hushållsavfall", och `/matavfall-i-stockholm` har knappen "Boka upphämtning av matavfall", samtidigt som restaurangsidan korrekt säger att matavfall bara hämtas av kommunens entreprenör. Hushållens restavfall och matavfall är kommunalt monopol i Stockholm (SVOA). Texterna bör skrivas om till det ni faktiskt gör: verksamhetsavfall, rådgivning om abonnemang, kärl och soprum. Obs: även startsidans huvudkort har "Matavfall på begäran" i fraktionslistan, det är min formulering och bör tas bort om ni inte hämtar matavfall.
6. **Prisuppgifter krockar.** Container: byggsidan säger 5 till 30 kubik, containersidorna 10 till 30. Byggsidans FAQ säger 4 500 till 5 000 kr för 20 kubik blandat, prissidan säger utställning 800 till 1 400 kr plus hemtagning 800 till 1 400 kr plus 180 till 1 900 kr per ton, och containersidans FAQ säger att transporten ingår i priset. Välj en prismodell och använd den överallt. Övriga priser att bekräfta: grovavfall från 275 kr, bortforsling från 285 kr per kubikmeter, byggsäck 600 till 1 500 kr, kärltvätt 650 till 895 kr framkörning och 225 till 275 kr per kärl, soprumstvätt 1 200 till 1 800 kr, kontorsåtervinning 145 till 195 kr per tömning och kärl.
7. **Ton och längd.** Många sidor är skrivna för sökord ("vår tjänst hämta återvinning Stockholm ser vi till att…") och upprepar samma budskap i tre till fyra stycken. Varje sida vinner på att kortas med ungefär en tredjedel och skrivas som till en styrelseledamot: vad får jag, vad kostar det, hur kommer jag igång. Sökordet behöver bara finnas i rubrik, ingress och en underrubrik.
8. **"Ungt företag".** Flera sidor kallar Avfallskonsulten ett ungt företag. Grundat 2017 är det snart tio år. Byt till "egen personal, egna bilar sedan 2017" eller liknande.
9. **Sidor utan hero-bild och ingress:** `/om-oss`, `/produkter`, `/fastighetsnara-insamling` börjar direkt med en underrubrik. Skriv en ingress på två meningar till var och en och välj en bild (om oss: personalen; produkter: kärlskåp; FNI: miljörum).
10. **Stavfel och kopieringsfel** finns listade per sida nedan. Vanligast: "BRF" och "brf" blandat, "istället" och "i stället", bindestreck som visas i början av punktlistor (brf-sidan, kontorssidan), rubriker som hamnat på fel sida.

## 2. Tekniska fel från min konvertering (rättar när du säger till)

- `/atervinning-stockholm` har två länkar med inledande snedstreck (`/atervinningsguide` och `/atervinnings_for_foretag_och_verksamheter`, den senare med stavfel i exporten). De fungerar inte på staging och den andra inte alls.
- `/atervinning_fastighet_och_brf` och `/kontorsatervinning` visar lösa bindestreck i punktlistor (exportens "**-Källsortering**").
- `/kontakt`: "Hitta hit" länkar till Solkraftsvägen 16A på Google Maps, sidfoten säger 14 A. Vilket är rätt?
- `/tradgardsavfall-stockholm`: rubriken "Vad ingår i våra tjänster för återvinning BRF?" är inklistrad från brf-sidan.
- `/matavfall-i-stockholm`: "Kontakta oss om ni vill att vi ska hämta era grovsopor!" är inklistrad från grovsopssidan.

## 3. Sida för sida

### /atervinning-stockholm (huvudsida för återvinning, hög prioritet)
- Ingressen handlar om kärltvätt och dålig lukt, inte om hämtning av återvinning. Skriv ny ingress om förpackningshämtning för brf i Stockholm och Lidingö.
- Sidan är en bra hubb (brf, kontor, företag) men saknar FNI 2027, Lidingö, pris och "så funkar det". Lägg in samma tre steg som på startsidan.
- "hyra en container i Stockholm" länkar till bygg- och trädgårdssidan, inte containersidan.
- Avsnitten "Vad kan återvinnas" och "Att tänka på när man sorterar" är allmän skolboksinformation som redan finns i återvinningsguiden. Flytta dit eller stryk.
- FAQ: 12 frågor, flera dubbletter (3 och 7 om hur ofta, 1 och 9 om bokning). Behåll sex.
- FAQ 2 lovar farligt avfall "i vissa fall", FAQ 5 lovar lysrör och kemikalier. Bekräfta.

### /atervinning_fastighet_och_brf (hög prioritet)
- Rubriken "Återvinning brf" är kort och sökordsstyrd. Förslag: "Återvinning för bostadsrättsföreningar i Stockholm och Lidingö".
- "Våra tjänster"-listan: ta bort bindestrecken och skriv hela meningar.
- Två avsnitt säger samma sak (Inredning och placering, Återvinningsabonnemang). Slå ihop.
- "Mer om återvinning brf" med "Framtiden för återvinning", "Miljöperspektivet" och "Kommunikation" är cirka 600 ord utfyllnad. Stryk eller korta till en punktlista med tips.
- FAQ 10 säger "ditt företags behov" på en brf-sida.
- Saknas: FNI 2027, Lidingö, pris per hämtning, vad som ingår (kärl, skyltar, tillsyn), ett kundexempel från projektsidan.

### /fastighetsnara-insamling (hög prioritet, er krok)
- Innehållet är bra och sakligt. Skriv en ingress och lägg en bild.
- Lägg till ett konkret avsnitt "Så hjälper vi er brf att klara 2027" med de tre stegen, exempel på kärluppsättning per antal lägenheter (ni har en schablon i offertverktyget) och en offert-CTA.
- "fram till 2026 kan de fortfarande använda lättillgängliga insamlingsplatser" bör uppdateras eftersom det nu är hösten 2026: "från 1 januari 2027 gäller kravet".
- Rubriken "Fastighetsnära insamling 2027 - Ny lagändring" kan bli "Fastighetsnära insamling 2027: det här gäller för er fastighet".

### /atervinning_for_foretag_och_verksamheter
- Bra och kort. FAQ 1 nämner hushållsavfall och organiskt avfall för företag, stryk det.
- Lovar farligt avfall, sortering av byggavfall på plats och energiåtervinning. Bekräfta.
- Saknar pris och exempel på kunder (kontor, restaurang, butik).

### /atervinningsforetag-stockholm
- Helt överlappande med startsidan och företagssidan, utan egen information. Förslag: korta till en halv sida som berättar om företaget som återvinningsföretag (egen personal, egna bilar, auktorisationer, Reco) och länkar vidare. "24 till 48 timmar" i FAQ 5 bör bekräftas.

### /atervinningsguide
- Bra, nyttig och lätt att läsa. Behåll. Två små saker: i guiden står att keramik och glödlampor inte ska i glaset, bra, men att "alla plasttyper återvinns på samma sätt" stämmer inte riktigt, skriv "alla plastförpackningar sorteras som plast". Textilier: sedan 2025 ska textil samlas in separat i kommunerna, uppdatera stycket.

### /avfallshantering-restaurang
- Rubriken "Hantering av matavfall och organiskt avfall" följs bara av en mening om kommunens entreprenör. Skriv om till ett stycke: "Matavfall hämtas av kommunens entreprenör. Vi hjälper er att välja rätt abonnemang och kärl, och vi hämtar allt annat."
- FAQ 3 säger att ni erbjuder lösningar för organiskt avfall, vilket motsäger raden ovanför.
- Stryk "Hur fungerar vår process" och "Varför välja oss", de är identiska med bortforslingssidans.

### /bortforsling (huvudsida för engångshämtning)
- Bra prisavsnitt. FAQ 3 och 5 är samma fråga, 1 och 6 överlappar. Behåll fem.
- "Varför välja Avfallskonsulten" och "Kontakta oss" säger samma sak, slå ihop.
- "samma dag eller inom 24 timmar" bekräfta.

### /hamta-skrap-stockholm
- Kopia av bortforslingssidan med ordet skräp. Ge den ett eget syfte (till exempel "liten mängd, snabb hämtning, fast pris") eller korta till 200 ord som länkar till bortforsling.

### /tomma-dodsbo
- Bra idé och bra ton. Men FAQ 3 ("Kan ni bära ut möbler") har svaret till fråga 4, och fråga 4 ("farligt avfall") har svaret om att bära ut möbler. Byt plats.
- Lägg till vad som skiljer från bortforsling: hänsyn, nycklar, städning efteråt, intyg till dödsboet, pris per lägenhet.

### /bygg-och-tradgardsavfall
- "Byggsäckar som bygavfallsalternativ": stavfel, ska vara byggavfallsalternativ.
- Container 5 till 30 kubik här, 10 till 30 på containersidorna.
- FAQ om containerpris krockar med prissidan, se punkt 6 ovan.
- Rubriken säger byggavfall men sidan heter bygg och trädgård, trädgården nämns knappt. Länka tydligt till trädgårdssidan.

### /hamta-byggsackar
- Under "Hushållsavfall" står att matavfall och förpackningar kan läggas i byggsäck. Det bör inte stå så, stryk hela hushållsavfallsavsnittet.
- FAQ 1 säger att det finns "säckar för farligt avfall", men avsnittet ovanför säger att farligt avfall inte får läggas i byggsäck. Stryk FAQ 1.
- "small, medium och large" i FAQ 4: skriv storlekar i liter eller kubik.
- Stegen under "Hur funkar det" har olika skiljetecken (bindestreck, kolon). Gör lika.

### /hamta-grovsopor-jarfalla, -lidingo, -norrtalje, -sollentuna, -sundbyberg, -taby
- Se punkt 2. Dessutom: listan "Vi har avtal med dessa kommuner" saknar Stockholm, Solna och Danderyd som startsidan räknar in. Hämtar ni verkligen grovsopor i Norrtälje regelbundet? Om inte, överväg att låta den sidan vara kort och ärlig.
- FAQ 9 till 12 säger "i Stockholm" på alla kommunsidor.

### /hamtning-av-restavfall-stockholm
- Se punkt 5. Erbjud restavfall för verksamheter (kontor, butik, restaurang) och skriv tydligt att hushållens restavfall sköts av kommunen. "Industriellt restavfall" och "modern teknik" bör strykas om det inte är något ni gör.
- FAQ 6 har ett tankstreck kvar i exporten, redan ersatt vid bygget.

### /hyra-container-stockholm och /hyra-container-blandat-avfall-pris
- Två sidor om samma sak med motstridiga uppgifter: transport "ingår vanligtvis i priset" på den ena, debiteras separat på den andra. "Hyr enkelt online" finns inte, ni har ett formulär. "Minsta hyresperiod en vecka" och "låsbara containrar" bekräfta.
- Förslag: huvudsidan beskriver storlekar, placering, regler och vad man får slänga; prissidan behåller prismodellen och en räkneexempel-tabell (10, 20, 30 kubik). Ta bort upprepningarna "Mer om våra containrar", "Anpassade lösningar", "Smidigt och miljövänligt".
- "Avfallskonsultenär" (ihopskrivet) på prissidan.

### /karltvatt
- Bra sida med riktiga priser. Prisstycket upprepas ordagrant två gånger (under rubriken och under "Vad påverkar priset"). Behåll ett.
- "Steg 3" säger "ett viktigt när man tvättar sopkärl", ord saknas.
- "minst en gång per månad" i texten, "2 till 4 gånger per år" i FAQ 7. Välj ett råd.

### /kontakt
- Bara tre rader. Lägg till adress, karta, öppettider, org.nr, vad som händer efter att man skickat formuläret, och gärna ett foto. Rätta adressen (14 A eller 16A).

### /kontorsatervinning
- Bra sida, bra struktur. Punktlistan under "Exempel på avfall" har lösa bindestreck. "BOKA Platsbesök" har fel versaler.
- Lovar rapportering med statistik, utbildningar och affischer. Bekräfta att ni gör det.
- FAQ 1 till 7 är allmän information om kontorsåtervinning, inte om er tjänst. Byt ut hälften mot frågor om pris, uppstart och kärl.

### /matavfall-i-stockholm
- Se punkt 5. Byt knappen "Boka upphämtning av matavfall" mot "Rådgivning om matavfall" och skriv att SVOA hämtar men att ni hjälper med kärl, skyltar, soprum och abonnemang.
- Felaktig CTA om grovsopor mitt i sidan.
- Bra förklaring av biogas och biogödsel, behåll.

### /om-oss
- Behöver ingress, bild och mer konkret innehåll: grundat 2017, antal bilar och anställda, auktoriserad i nio kommuner, Reco 4,9, kontoret på Solkraftsvägen. "Skrubba och Järfälla", stämmer Järfälla fortfarande?
- "Vår kundbas består idag av både små och stora fastighetsägare, företag, som värdesätter" har en kommateringsmiss.
- CSR-avsnittet: stämmer sponsringarna (Spårvägen Fotboll, Hammarby Fotboll, Hammarby Bandy) i dag?
- "ungt och drivkraftigt företag", se punkt 8.

### /produkter
- Kort och okej. "ett enkelt sätta att bygga in" ska vara "sätt". Lägg till priser eller "från"-pris, och en bild per produkt (finns i site-kopia). Produktbladet (pdf, 1 MB) är från gamla sajten, kontrollera att det är aktuellt.

### /projekt
- Alviksskolan: andra halvan av texten (sopkarusell, halverad driftkostnad) är inklistrad från Brf Narva och handlar inte om skolan. Stryk de två styckena.
- Brf Markisen: "renovera deras soprum" länkar till kärltvätt, ska gå till renovera-soprum.
- "Stockholm och vatten AB" ska vara Stockholm Vatten och Avfall.
- Bra sida i övrigt, lägg gärna till ett återvinningsprojekt hos en brf eftersom det är huvudtjänsten nu.

### /radgivning
- Avsnittet om förpackningar säger "Exakta detaljer är ännu inte klara, en fråga om när, inte om". Det är inaktuellt, kravet är 1 januari 2027. Skriv om och länka till FNI-sidan.
- Matavfallsdatumen (2023, 2024) stämmer men kan kortas till "sedan 2024 obligatoriskt".
- Nämn att rådgivning och platsbesök är kostnadsfritt, och vad en avfallsutredning kostar.

### /renovera-soprum
- Okej men generisk. Lägg in ett konkret exempel från projektsidan (Narva, Högbergsgatan), riktpris och bilder före och efter (finns i site-kopia: soprum_1fore, soprum_1efter).
- FAQ 4 "1 till 2 veckor" bekräfta.

### /sekretesshantering
- "sekkretesspapper" stavfel. "destruktioncenter" ska vara destruktionscenter, och är det ert eget? "elektroniska dokument" förstör ni knappast, stryk.
- Privatpersonavsnittet: hämtar ni verkligen från privatbostäder? Annars stryk.
- Saknar pris per kärl och hur ofta kärlen töms.

### /sophamtning-stockholm-foretag
- Nästan samma som företagssidan. "Organiskt avfall och emballage" lovar matavfall, se punkt 5. "specialanpassade fordon" och "fordon med låga utsläpp" bekräfta.

### /tidningsatervinning
- Tunn sida med avsnittet "Varför återvinna tidningar" två gånger och tre nästan identiska fördelspunkter. Korta till en halv sida: ni hämtar tidningar och returpapper i samma abonnemang som förpackningar, pris, länk till återvinningssidan.

### /forpackningsinsamling
- Generisk text riktad till "företag och organisationer" fast sidan i praktiken handlar om samma sak som brf-återvinningen. Påståendet om "specialiserade processer för kompositförpackningar" bör strykas. Förslag: gör sidan till en kort förklaring av förpackningsinsamling för fastigheter med länk till FNI-sidan och offert.

### /tradgardsavfall-stockholm
- Ingressen upprepas ordagrant i första avsnittet. "träddgårdsavfall" stavfel. Fel rubrik om brf (se punkt 2 i tekniska fel). FAQ 2 och 5, 3 och 6, 7 och 12 är dubbletter. Behåll sex frågor.
- Saknar pris (ni har 375 kr per kubikmeter i andra sammanhang, bekräfta vad som ska stå).

## 4. Frågor till dig innan texterna skrivs om

1. Hämtar ni matavfall åt någon alls, eller bara rådgivning om SVOA-abonnemang?
2. Hämtar ni hushållens restavfall någonstans (till exempel i kommuner där ni är upphandlade)?
3. Vilka priser ska stå på sajten, och ska container ha en prismodell (utställning plus hemtagning plus behandling)?
4. Stämmer "100 % fossilfria transporter", "låsta transportfordon" och "tillstånd för farligt avfall"?
5. Norrtälje: kör ni dit, eller ska den sidan bli en kort hänvisning?
6. Adressen: Solkraftsvägen 14 A eller 16A?
7. Ska privatpersoner fortfarande vara en målgrupp på bortforsling, dödsbo och skräp, eller styr vi dem till Wasteless som i mejlsvaren?

## 5. Föreslagen ordning

1. Rätta de tekniska felen och kopieringsfelen (en timme, påverkar inte innehållet i sak).
2. Skriv om de tre prioriterade sidorna: återvinning Stockholm, brf, FNI 2027, med Lidingö, 2027, pris och tre steg.
3. Besluta om matavfall och restavfall, skriv om de sidorna.
4. Ena priserna på container, bygg och trädgård.
5. Slå ihop eller korta dubbletterna (skräp, dödsbo, återvinningsföretag, sophämtning företag, tidningar, förpackningsinsamling).
6. Ge kommunsidorna unikt innehåll, Lidingö först.
7. Om oss, kontakt och produkter får ingress, bild och konkreta uppgifter.
