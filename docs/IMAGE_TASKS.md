# Bildeoppgaver – illustrasjoner som mangler

> Samme liste som GitHub-issue #41 (https://github.com/XS227/Numerologist/issues/41). Hold filen og issuet i sync; kryss av her når et bilde er lagt inn.

Liste over illustrasjoner som mangler på numerologist.setai.no. Noen steder brukes plassholdere, andre steder gjenbrukes samme bilde flere ganger. Generer bildene under, legg dem i repoet og koble dem inn der det står under **Kobles inn**.

## Felles krav (gjelder alle bilder)

- **Format:** `.webp`, **1536 × 1024** (3:2), kvalitet ~80, under 350 KB
- **Mappe:** `tall_project/static/journey/images/`
- **Stil:** samme som eksisterende bilder (`origins.webp`, `traditions.webp`, `modern.webp`, `name-method.webp`): maleraktig og filmatisk, natt/skumring, dyp petrol/teal (#092426) med varmt gull- og stearinlys (#c6a775), rolig og høytidelig, mye mørkt rom til venstre så tekst kan ligge oppå
- **Ingen** tekst, bokstaver, logoer eller vannmerker i bildet (tall kun der prompten ber om det)
- **Ingen** gjenkjennelige ekte personer. Mahsa/Bita-artikkelen skal være symbolsk, uten ansikter
- Etter at du har lagt til bildene: `collectstatic`, og bump `?v=` på CSS/JS der malen endres

---

## A. WOW-signal-artikkelen (bruker nå CSS-plassholdere)

Maler: `tall_project/templates/articles/detail_wow_signal.html` og kapitler i `articles/wow_journey.py`.
**Kobles inn:** bytt `<div class="j-parallax j-placeholder" …>` med `<img class="j-parallax" src="{% static 'journey/images/<fil>.webp' %}" data-speed="…" alt="…">`, og fjern `.j-placeholder`-CSS-en.

- [x] `wow-hero.webp`: Arecibo-radioteleskopets enorme parabol i en jungeldal om natten under Melkeveien, gull-lys fra instrumenthuset
- [x] `wow-arecibo.webp`: Arecibo-meldingen 1974: stråle av gyllent lys som sendes fra parabolen mot en stjernehop (M13), ingen piksler/tekst
- [x] `wow-wow.webp`: 1977: en gammel papirutskrift fra en radiomottaker på et skrivebord i lampelys, en rød blekkring rundt en kolonne (ingen lesbar tekst)
- [x] `wow-interval.webp`: rytme og intervaller: konsentriske gullbølger over mørkt hav, som en puls
- [x] `wow-frb.webp`: raske radioutbrudd: et kort, skarpt gullglimt i en fjern galakse over et radioteleskop-felt
- [x] `wow-atlas.webp`: kosmisk atlas: gammelt stjernekart i messing og papir, sirkler og linjer som knytter punkter
- [x] `wow-reflection.webp`: refleksjon: en person sett bakfra ved et vindu som ser ut på stjernehimmelen, notatbok i fanget

## B. Coverbilder for artiklene (i dag bare typografiske «plakater»)

7 artikler (WOW-artikkelen har egne bilder i A).

Brukes som hero på artikkelsiden og som thumbnail i `/articles/` og på forsiden.
**Kobles inn:** `articles/thumbnails.py` (legg til `image`-felt) + `list.html`, `index.php` (`numerologist_latest_articles`) og hero i `static/journey/article.css`.

- [x] `article-navn-numerologi.webp`: tre-bokstavbrikker som staver et navn på et skrivebord, tall svevende i gull over hver brikke (tallene 1–9 er ok)
- [x] `article-master-33.webp`: tallet 33 formet av stearinlys eller stjerner over en stille innsjø, varm omsorgsfull stemning
- [x] `article-shahnameh.webp`: persisk manuskript (Shahnameh-stil) med miniatyrmaleri og gullornamentikk, oppslått i lampelys, ingen lesbar skrift
- [x] `article-mahsa-bita.webp`: SYMBOLSK, ingen ansikter: to stearinlys side om side foran et vindu, et hårbånd/skjerf i bris, to fjerne kontinenter som silhuetter
- [x] `article-creative-research.webp`: forskerbord: skisser, passer, fargeblyanter og tallmønstre, «laboratorium for kreativ praksis»
- [x] `article-tallene-i-koranen.webp`: Koranen som tallstruktur: et oppslått manuskript med gull-illuminert ornamentikk på et lesepult (rahle) i lampelys, over siden svever tre rolige lysbuer som en puls (lav, midt, høy). Ingen lesbar skrift, ingen vers
- [x] `article-profeten-muhammads-tall.webp`: **HELT ABSTRAKT – ingen person, silhuett, ansikt, hånd eller skikkelse av noe slag** (islamsk tradisjon avbilder ikke profeten). Motiv: ørkennatt over Mekka-dalen sett langt unna, stjernehimmel der to lyse punkter står side om side som et stille «11», geometrisk islamsk stjernemønster (girih) i gull svakt over himmelen. Ingen tekst, ingen kalligrafi av navnet

## C. Kalkulatorer (gjenbruker nå bilder fra andre sider)

**Kobles inn:** `tall_project/templates/pages/calculators.html` (kort-bildene), `index.php` (`$calcTiles`) og `image`/`split_image` i `tall_project/learning.py`.

- [x] `calc-soul-urge.webp`: sjelstall/vokaler: et hjerteformet lys inni et åpent navnebrev, mykt og innadvendt
- [x] `calc-personality.webp`: personlighetstall/konsonanter: en dør på gløtt med varmt lys, en skikkelse på vei inn (bakfra)
- [x] `calc-methods.webp`: metode/reduksjon: gammel regnetavle eller kuleramme med gullkuler, tall som «kokes ned» i en spiral
- [x] `calc-compatibility.webp`: kompatibilitet: to stjernestier som møtes og flettes over en fjellsjø
- [x] `calc-personal-year.webp`: personlig år: en solur/årssirkel med tolv felt i gull, årstider rundt

## D. Tallsidene `/numbers/1/` … `/numbers/33/` (valgfritt, i dag CSS-paneler med tallet)

**Kobles inn:** `tall_project/templates/pages/number-detail.html` (`.n-figure`-panelene). Behold det store tallet i heroen.

- [x] `number-1.webp` … `number-9.webp`, `number-11.webp`, `number-22.webp`, `number-33.webp`: ett symbolsk motiv per tall, i samme stil. Temaene er: 1 Initiativ, 2 Samarbeid, 3 Uttrykk, 4 Struktur, 5 Frihet, 6 Omsorg, 7 Fordypning, 8 Realisering, 9 Fullføring, 11 Inspirasjon, 22 Byggmester, 33 Mesterlærer. Ingen tall i selve bildet.

## E. Forsiden og Åse-siden

- [x] `home-hero.webp`: forsidens hero-bakgrunn: nattlig bibliotek eller observatorium, gulllys, tall 1–9 svakt glødende i luften, mørkt til venstre for tekst. **Kobles inn:** `.hero` i `assets/home.css` (bakgrunnsbilde med mørk gradient over)
- [x] `ase-method.webp`: erstatter det lavoppløste Vitruvius-banneret (`assets/images/about-hero.jpg`, 676×255) på `/ase-steinsland/`: pytagoreisk harmoni med monokord, geometri og tallrekker på pergament i gull/sepia. **Kobles inn:** `.ase-figure` i `tall_project/templates/pages/ase-steinsland.html`

## ⚠️ Ikke AI-generer

- **Portrett av Åse:** `assets/images/ase-steinsland.jpg` er bare **259×240 px** og blir uskarpt i de store sirklene. Vi trenger et **ekte foto** av Åse i høyere oppløsning (minst 800×800, kvadratisk, ansiktet midt i). Det skal ikke lages med AI.

---

Laget ut fra gjennomgang av malene på serveren 2026-09-22.


