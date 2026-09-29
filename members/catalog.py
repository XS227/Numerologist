from __future__ import annotations

PACKAGE_CATALOG = {
    "builder": {
        "title": "Din numerologiske analyse",
        "price": 227,
        "kind": "modular",
        "summary": "Kjerneanalyse med valgfrie kalkulatormoduler og fremtid fra 1 til 36 måneder.",
        "sections": [
            "Kjerne: navnetall, vokaltall, konsonanttall, livsvei og fødselsdag",
            "Valgfrie moduler fra Åses komplette kalkulatorbibliotek",
            "Fremtid kan legges til for 1, 3, 6, 12, 24 eller 36 måneder",
            "Kjøpte moduler åpnes samlet på Min side",
        ],
    },
    "ase227": {
        "title": "ÅSE 227 Edition",
        "price": 227,
        "kind": "digital",
        "summary": "Komplett digital motorrapport med hele tallkartet, personlig fortelling og timing.",
        "sections": [
            "Personlig åpning og hovedmønster",
            "Navnetall, vokaltall, konsonanttall og nåværende navn",
            "Skjebnetall, fødselsdagstall, broer og balansetall",
            "Styrker, vekstområder, jobb og nære relasjoner",
            "Personlig år, måned, transitter og essenstall",
            "Utviklingstrinn, livsperioder, utfordringstall og realiseringstall",
            "Adresse, telefon og partnerlag når data finnes",
            "Komplett tallkart og PDF-visning",
        ],
    },
    "personlighet": {
        "title": "Personlighetsanalyse",
        "price": 698,
        "kind": "human",
        "summary": "Digital grunnrapport med motoren med plass til Åses personlige utdyping.",
        "sections": [
            "Kjerneidentitet og personlighet",
            "Indre drivkraft og ytre uttrykk",
            "Styrker og vekstområder",
            "Karmiske gjelds- og læringstall",
            "Symbolsk helseprofil",
            "Lykketall og viktige gjentakelser",
            "Åses personlige kommentar og syntese",
        ],
    },
    "fremtid2": {
        "title": "2 års Fremtidsanalyse",
        "price": 698,
        "kind": "human",
        "summary": "Digital timingrapport med to år, månedslinje og Åses fordypning.",
        "sections": [
            "Nå-situasjonen i tallkartet",
            "Personlig år for år 1 og år 2",
            "Personlige måneder",
            "Fysisk, mental og spirituell transitt",
            "Essenstall og aktive tema",
            "Viktige skifter og overlapp mellom sykluser",
            "Åses personlige fremtidstolkning",
        ],
    },
    "partner": {
        "title": "Partneranalyse + 1 år",
        "price": 798,
        "kind": "human",
        "summary": "To tallkart, kompatibilitetskart og relasjonens timing.",
        "sections": [
            "Person A – kjernekart",
            "Person B – kjernekart",
            "Navnetall-kompatibilitet",
            "Skjebnetall-kompatibilitet",
            "Likheter, forskjeller og kommunikasjonsmønstre",
            "Relasjonens aktive år og måneder",
            "Åses personlige relasjonssyntese",
        ],
    },
    "komplett1": {
        "title": "Komplett analyse + 1 år",
        "price": 998,
        "kind": "human",
        "summary": "Full personlig analyse med ett års fremtidslag.",
        "sections": [
            "Alt fra Personlighetsanalyse",
            "Alle transitter og essenstall",
            "Fire utviklingstrinn og tre livsperioder",
            "Fire utfordringstall og realiseringstall",
            "Personlig år og månedslinje i 12 måneder",
            "Åses fullstendige syntese",
        ],
    },
    "komplett2": {
        "title": "Komplett analyse + 2 år",
        "price": 1098,
        "kind": "human",
        "summary": "Full personlig analyse med to års fremtidslag.",
        "sections": [
            "Alt fra komplett personlig analyse",
            "To personlige år",
            "24 måneders timing",
            "Transitter og essenstall gjennom perioden",
            "Overganger mellom større livssykluser",
            "Åses fullstendige syntese",
        ],
    },
    "komplett3": {
        "title": "Komplett analyse + 3 år",
        "price": 1198,
        "kind": "human",
        "summary": "Den mest omfattende Åse-analysen med tre års timing.",
        "sections": [
            "Alt fra komplett personlig analyse",
            "Tre personlige år",
            "36 måneders timing",
            "Transitter og essenstall gjennom perioden",
            "Utviklingstrinn og langsiktig retning",
            "Åses fullstendige syntese",
        ],
    },
    "veiledning15": {
        "title": "Veiledningssamtale 15 min",
        "price": 360,
        "kind": "human",
        "summary": "Digital forberedelsesside før samtalen og notater etterpå.",
        "sections": [
            "Kort automatisk kart før samtalen",
            "Tre viktigste mønstre akkurat nå",
            "Spørsmål du vil ta opp med Åse",
            "Samtalenotater",
            "Lenker til relevante tall og artikler",
        ],
    },
    "familie3": {
        "title": "3 komplette analyser + 1 år",
        "price": 2994,
        "kind": "human",
        "summary": "Tre separate digitale rapporter med ett års timing for hver person.",
        "sections": [
            "Person 1 – komplett rapport + 1 år",
            "Person 2 – komplett rapport + 1 år",
            "Person 3 – komplett rapport + 1 år",
            "Felles oversikt over de tre rapportene",
        ],
    },
}

ACADEMY_LEVELS = [
    {
        "level": 1,
        "title": "Tallene 1–9",
        "subtitle": "Lær alfabetet før du tolker setningene.",
        "description": "Bygg et presist språk for grunnenergiene 1–9 og lær å skille symbolsk tolkning fra generiske personlighetstekster.",
        "lessons": [
            "Kjernen i 1–9",
            "Styrke, skygge og balansert uttrykk",
            "Reduksjon og sammentall",
            "Hvordan lese et tall i kontekst",
        ],
        "homework": "Før en 7-dagers talljournal. Velg ett tall du møter hver dag, og skriv én konkret observasjon uten å tolke først. Legg deretter til numerologisk tolkning som et eget lag.",
        "premium": ["Tall 1–9: praktiske case", "Feil nybegynnere gjør i reduksjon"],
        "articles": ["/numbers/1/", "/numbers/8/", "/calculation-methods-overview/"],
    },
    {
        "level": 2,
        "title": "Navn og identitet",
        "subtitle": "Når bokstaver blir til et menneskelig kart.",
        "description": "Lær navnetall, vokaltall, konsonanttall, nåværende navn, hjørnestein, broer og karmiske læringstall.",
        "lessons": [
            "Pythagoreisk bokstavtabell",
            "Fødselsnavn vs. nåværende navn",
            "Vokal og konsonant som indre/ytre lag",
            "Broer, hjørnestein og karmiske læringstall",
        ],
        "homework": "Analyser tre navn: ditt eget og to frivillige case. Skriv først beregningen, deretter tolkningen, og marker tydelig hva som er observasjon og hva som er symbolsk lesning.",
        "premium": ["Navnedeterminisme – fordypning", "Slik syntetiserer Åse tre navnelag"],
        "articles": ["/articles/navn-navnedeterminisme/", "/articles/barn-og-navn/", "/compute-name-vowel-consonant/"],
    },
    {
        "level": 3,
        "title": "Tid og livssykluser",
        "subtitle": "Fra hvem du er til når et tema blir aktivt.",
        "description": "Arbeid med personlig år/måned, transitter, essenstall, utviklingstrinn, livsperioder og utfordringstall.",
        "lessons": [
            "Personlig år og måned",
            "Fysisk, mental og spirituell transitt",
            "Essenstall",
            "Pinnacles, livsperioder og utfordringer",
        ],
        "homework": "Bygg en 24-måneders tidslinje for én case. Marker minst tre steder der korte og lange sykluser overlapper.",
        "premium": ["Timing uten spådomsspråk", "Case: når tre sykluser peker samme vei"],
        "articles": ["/personal-year-number/", "/essence-number/", "/pinnacle-cycles/"],
    },
    {
        "level": 4,
        "title": "Relasjoner og syntese",
        "subtitle": "To mennesker er mer enn én kompatibilitetsbokstav.",
        "description": "Lær å sammenligne to komplette kart og bruke Åses A/B/C/D/A-D-tabeller som ett lag, ikke som fasit.",
        "lessons": [
            "Kompatibilitetstabellene",
            "Navnelag vs. livsveilag",
            "Sterk polaritet A/D",
            "Slik snakker du om relasjoner uten dom",
        ],
        "homework": "Lag en partneranalyse der minst ett lag er harmonisk og ett lag er krevende. Skriv en balansert muntlig oppsummering på maks 400 ord.",
        "premium": ["Arbeidsforhold vs. nære relasjoner", "Casebibliotek for blandede resultater"],
        "articles": ["/articles/tall-og-kompatibilitet/", "/partner-profile/", "/articles/valentinsdagens-tall/"],
    },
    {
        "level": 5,
        "title": "Become a Numerologist",
        "subtitle": "Fra beregning til profesjonell konsultasjon.",
        "description": "Syntetiser hele kartet, bygg en konsultasjon, arbeid etisk og lever en avsluttende case.",
        "lessons": [
            "Den første 10-minutters lesningen",
            "Hvordan prioritere 25+ tall",
            "Spørsmål, språk og etikk",
            "Rapportstruktur og konsultasjon",
        ],
        "homework": "Avsluttende case: full ÅSE Edition-lesning for en samtykkende voksen, med beregningsvedlegg, 800–1200 ord syntese og en 10-minutters muntlig presentasjon.",
        "premium": ["Åses konsultasjonsstruktur", "Avsluttende case-mal", "Etikk og profesjonelle grenser"],
        "articles": ["/ase-edition/", "/calculators/", "/articles/"],
    },
]


PREMIUM_RESOURCES = {
    1: {
        "case-1-9": {
            "title": "Tall 1–9: praktiske case",
            "lead": "Samme tall ser forskjellig ut etter posisjon, alder og kontekst.",
            "body": [
                "Et 8-tall i navnet bør ikke leses identisk med 8 som personlig år. Symbolet er det samme, men rollen er forskjellig. Navnet beskriver uttrykk og identitet; årstallet beskriver timing.",
                "Når du øver, skal du alltid kunne svare på tre spørsmål: Hvilket tall ser jeg? Hvor i kartet står det? Hva er det konkrete mennesket eller situasjonen som skal forstås?",
                "En god numerologisk formulering er spesifikk nok til å kunne gjenkjennes, men åpen nok til at du ikke later som symbolet er en medisinsk, psykologisk eller statistisk diagnose.",
            ],
        },
        "reduction-errors": {
            "title": "Feil nybegynnere gjør i reduksjon",
            "lead": "Regnefeil forplanter seg gjennom hele kartet.",
            "body": [
                "Skill mellom rå sum, sammentall og rot. Dersom metoden bevarer 11, 22 eller 33 i en bestemt posisjon, må dette skje konsekvent.",
                "Navn bør beregnes med samme regel gjennom hele analysen. Å bytte mellom å summere hele navnet flatt og å redusere navnedeler først kan gi ulike resultater.",
                "Skriv alltid mellomregningen i case-arbeid. Da kan både du og klienten etterprøve beregningen.",
            ],
        },
    },
    2: {
        "name-determinism": {
            "title": "Navnedeterminisme – fordypning",
            "lead": "Navn påvirker sosial identitet, men numerologisk symbolikk må holdes adskilt fra dokumenterbar årsak.",
            "body": [
                "Navn kan påvirke hvordan andre møter oss, hvordan vi presenterer oss og hvilke assosiasjoner som følger oss. Det er et sosialt lag som kan undersøkes empirisk.",
                "Numerologi legger et symbolsk tallag oppå dette. Academy lærer deg å si tydelig hvilket lag du snakker om, i stedet for å blande dokumenterbare effekter og spirituell tolkning.",
            ],
        },
        "three-name-layers": {
            "title": "Slik syntetiserer Åse tre navnelag",
            "lead": "Navnetall, vokaltall og konsonanttall bør bli én fortelling.",
            "body": [
                "Start med helheten: navnetallet. Gå deretter innover til vokalene og utover til konsonantene. Spør om de tre lagene forsterker hverandre eller trekker i forskjellige retninger.",
                "Det mest interessante er ofte avstanden mellom indre behov og ytre uttrykk, ikke om ett tall isolert er 'godt' eller 'dårlig'.",
            ],
        },
    },
    3: {
        "timing-language": {
            "title": "Timing uten spådomsspråk",
            "lead": "Sykluser skal gi orientering, ikke falsk sikkerhet.",
            "body": [
                "Et personlig år beskriver et tema eller klima, ikke en garantert hendelse. Formuler deg derfor med ord som 'tendens', 'tema', 'invitasjon' og 'periode for'.",
                "Når flere tidslag peker mot samme tema, kan du fremheve at signalet er sterkere i kartet uten å gjøre det til en sikker prediksjon.",
            ],
        },
        "cycle-overlap": {
            "title": "Case: når tre sykluser peker samme vei",
            "lead": "Personlig år, essens og transitt kan sammen skape et tydeligere mønster.",
            "body": [
                "Begynn med det langsomste laget, legg deretter på personlig år og til slutt måned/transitt. Slik unngår du å la et kort øyeblikk overskygge den lange utviklingen.",
                "Skriv en syntese på tre nivåer: langsiktig retning, årets arbeid og hva som er aktivt akkurat nå.",
            ],
        },
    },
    4: {
        "work-vs-love": {
            "title": "Arbeidsforhold vs. nære relasjoner",
            "lead": "Åses kompatibilitetstabeller er ikke identiske for jobb og privatliv.",
            "body": [
                "En kombinasjon kan fungere svært godt i arbeid fordi rollene er tydelige, men oppleves annerledes i en nær relasjon der behov, sårbarhet og forventninger er andre.",
                "Derfor må du alltid velge riktig kompatibilitetskontekst før du tolker bokstaven A, B, C, D eller A/D.",
            ],
        },
        "mixed-results": {
            "title": "Casebibliotek for blandede resultater",
            "lead": "Et godt navnelag og et krevende livsveilag er ikke en motsigelse.",
            "body": [
                "Blandede resultater er normale. De viser at ulike deler av relasjonen har ulik friksjon. Jobben din er å beskrive hvor flyten er naturlig og hvor bevisst kommunikasjon trengs.",
                "Unngå konklusjoner som 'dere passer' eller 'dere passer ikke'. Beskriv mønster, ikke dom.",
            ],
        },
    },
    5: {
        "consultation-structure": {
            "title": "Åses konsultasjonsstruktur",
            "lead": "En klient trenger en fortelling, ikke 28 enkeltresultater.",
            "body": [
                "Start med to eller tre mønstre som faktisk bærer kartet. Forklar hvorfor de er viktige før du går inn i detaljer.",
                "Flytt deretter fra identitet til styrker, friksjon, relasjoner og timing. Avslutt med hva klienten konkret kan observere eller arbeide med.",
            ],
        },
        "final-case": {
            "title": "Avsluttende case-mal",
            "lead": "Slik dokumenterer du beregning, syntese og muntlig presentasjon.",
            "body": [
                "Del innleveringen i fire deler: beregningsvedlegg, prioriterte hovedmønstre, skriftlig syntese og refleksjon over språk/etikk.",
                "En sensor skal kunne følge hvordan du gikk fra rå tall til formulering uten at viktige hopp skjules.",
            ],
        },
        "ethics": {
            "title": "Etikk og profesjonelle grenser",
            "lead": "Numerologi er et refleksjonsverktøy, ikke en erstatning for faglig rådgivning.",
            "body": [
                "Ikke diagnostiser helse, psykiske tilstander, juridiske problemer eller økonomisk risiko fra tall. Når slike tema kommer opp, hold deg til symbolsk refleksjon og anbefal relevant fagperson ved behov.",
                "Be om samtykke før du analyserer tredjeparter, særlig i undervisningscase. Anonymiser case som deles i Academy.",
            ],
        },
    },
}
