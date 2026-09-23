"""Bilingual, illustrated lessons accompanying the numerology journey."""

from intake.forms import LETTER_VALUES


def learning_content(slug, language):
    no = language in ("nb", "no", "nn")

    def t(en, nb):
        return nb if no else en

    common = dict(
        start=t("Explore this chapter", "Utforsk kapitlet"),
        back=t("Back to the journey", "Tilbake til reisen"),
        explore=t("Explore the next chapter", "Utforsk neste kapittel"),
        calculator=t("Try your own numbers", "Prøv dine egne tall"),
        perspective=t(
            "Numerology offers symbolic interpretations for reflection, not"
            " scientifically established descriptions of personality or "
            "predictions.",
            "Numerologi tilbyr symbolske tolkninger til refleksjon, ikke "
            "vitenskapelig etablerte beskrivelser av personlighet eller "
            "forutsigelser.",
        ),
        art=t("Original artistic illustration.", "Original kunstnerisk illustrasjon."),
        strengths=t("An invitation", "En invitasjon"),
        balance=t("Something to balance", "Noe å balansere"),
        read=t("Read about this number", "Les mer om dette tallet"),
        chart_title=t("One alphabet. Nine values.", "Ett alfabet. Ni verdier."),
        chart_caption=t(
            "Pythagorean letter values used on this website",
            "Pytagoreiske bokstavverdier brukt på dette nettstedet",
        ),
        value=t("Value", "Verdi"),
        letters=t("Letters", "Bokstaver"),
        note=t(
            "A calculation is reproducible. Its symbolic meaning is an interpretation.",
            "En beregning kan etterprøves. Den symbolske betydningen er en tolkning.",
        ),
        source=t(
            "Historical source: Stanford Encyclopedia of Philosophy",
            "Historisk kilde: Stanford Encyclopedia of Philosophy",
        ),
    )
    pages = {
        "general-interpretation": dict(
            kind="numbers",
            image="number-meanings",
            eyebrow=t("01 / Understand the numbers", "01 / Forstå tallene"),
            title=t("Meet the numbers.", "Bli kjent med tallene."),
            subtitle=t(
                "Nine themes. Many ways to reflect.",
                "Ni temaer. Mange måter å reflektere på.",
            ),
            intro=t(
                "Begin with the qualities associated with each number. Then "
                "consider where that number appears in a reading — a name and a"
                " birth date answer different questions.",
                "Begynn med egenskapene som forbindes med hvert tall. Se "
                "deretter på hvor tallet står i en analyse – et navn og en "
                "fødselsdato belyser ulike spørsmål.",
            ),
            alt=t(
                "Illustrated people beginning a journey, cooperating and "
                "building together",
                "Illustrerte mennesker som begynner en reise, samarbeider og "
                "bygger sammen",
            ),
            section_title=t(
                "Read a theme, not a label.", "Les et tema, ikke en merkelapp."
            ),
            section_body=t(
                "A number is not a verdict about who you are. Use these "
                "traditional associations as questions: where do I recognise "
                "this quality, and where could I find a better balance? No "
                "number is better than another.",
                "Et tall er ikke en dom over hvem du er. Bruk disse "
                "tradisjonelle assosiasjonene som spørsmål: Hvor kjenner jeg "
                "igjen egenskapen, og hvor kan jeg finne bedre balanse? Ingen "
                "tall er bedre enn andre.",
            ),
            masters=t(
                "11 · 22 · 33 — the master numbers", "11 · 22 · 33 – mestertallene"
            ),
            masters_body=t(
                "In this tradition, 11 is associated with inspiration, 22 with "
                "building and 33 with compassionate guidance. They also connect"
                " to 2, 4 and 6. They are not a ranking of people or a promise "
                "of special powers.",
                "I denne tradisjonen forbindes 11 med inspirasjon, 22 med "
                "gjennomføring og 33 med omsorgsfull veiledning. De har også "
                "forbindelser til 2, 4 og 6. De er ingen rangering av mennesker"
                " eller et løfte om spesielle evner.",
            ),
        ),
        "letter-value-chart": dict(
            kind="letters",
            image="letter-workshop",
            eyebrow=t("02 / From letters to numbers", "02 / Fra bokstaver til tall"),
            title=t(
                "Your name, letter by letter.", "Navnet ditt, bokstav for bokstav."
            ),
            subtitle=t("Make the method visible.", "Gjør metoden synlig."),
            intro=t(
                "A letter chart is a lookup table. Each letter has a value from"
                " 1 to 9. Learn the table, try a short name, and follow how the"
                " values come together.",
                "En bokstavtabell er en oppslagstabell. Hver bokstav har en "
                "verdi fra 1 til 9. Bli kjent med tabellen, prøv et kort navn "
                "og følg hvordan verdiene settes sammen.",
            ),
            alt=t(
                "Illustration of hands arranging wooden letter blocks beside a "
                "notebook",
                "Illustrasjon av hender som ordner bokstavbrikker ved en notatbok",
            ),
            section_title=t(
                "Start with the letters you actually use.",
                "Begynn med bokstavene du faktisk bruker.",
            ),
            section_body=t(
                "The Latin alphabet repeats through values 1–9. On this site Å "
                "has value 1, Æ has value 5 and Ø has value 6. Spaces separate "
                "name parts; punctuation has no numeric value. Ask Åse about "
                "names written in other alphabets instead of guessing a "
                "transliteration.",
                "Det latinske alfabetet går i runder gjennom verdiene 1–9. På "
                "denne siden har Å verdien 1, Æ verdien 5 og Ø verdien 6. "
                "Mellomrom skiller navnedelene; tegnsetting har ingen "
                "tallverdi. Spør Åse om navn i andre alfabeter fremfor å gjette"
                " en omskriving.",
            ),
            example_title=t("A small example: ADA", "Et lite eksempel: ADA"),
            example_body=t(
                "Look up each letter: A is 1, D is 4 and A is 1. Add the "
                "values. The name part ADA gives 6. With several name parts, "
                "calculate each part first.",
                "Slå opp hver bokstav: A er 1, D er 4 og A er 1. Legg sammen "
                "verdiene. Navnedelen ADA gir 6. Med flere navnedeler regner du"
                " ut hver del først.",
            ),
            formula="A + D + A → 1 + 4 + 1 → 6",
            detail_title=t(
                "Same letters, different questions.", "Samme bokstaver, ulike spørsmål."
            ),
            detail_body=t(
                "The expression number uses all supported letters. The "
                "soul-urge number uses vowels. The personality number uses "
                "consonants. Here Y, Æ, Ø and Å are counted as vowels, "
                "alongside A, E, I, O and U.",
                "Uttrykkstallet bruker alle støttede bokstaver. Sjelstallet "
                "bruker vokalene. Personlighetstallet bruker konsonantene. Her "
                "regnes Y, Æ, Ø og Å som vokaler sammen med A, E, I, O og U.",
            ),
        ),
        "compute-destiny-number": dict(
            kind="method",
            image="name-method",
            eyebrow=t("03 / Follow the calculation", "03 / Følg beregningen"),
            title=t("A name. A method. A number.", "Et navn. En metode. Et tall."),
            subtitle=t("Understand every step.", "Forstå hvert steg."),
            intro=t(
                "The destiny number is also called the expression number. It is"
                " derived from the name. In the method used here, each name "
                "part is reduced first — then the parts are combined.",
                "Skjebnetallet kalles også uttrykkstallet. Det beregnes fra "
                "navnet. I metoden som brukes her, reduseres hver navnedel "
                "først – deretter legges delene sammen.",
            ),
            alt=t(
                "Illustration of a woman working through separate rows in a notebook",
                "Illustrasjon av en kvinne som arbeider gjennom separate rader "
                "i en notatbok",
            ),
            section_title=t("The order matters.", "Rekkefølgen betyr noe."),
            section_body=t(
                "Åse has worked with personal numerology analyses since 1997. "
                "The site documents a method that treats first, middle and last"
                " names as separate parts. That preserves the steps behind the "
                "result and helps avoid misleading master-number results from "
                "one flat sum.",
                "Åse har arbeidet med personlige numerologiske analyser siden "
                "1997. Nettstedet dokumenterer en metode som behandler fornavn,"
                " mellomnavn og etternavn som egne deler. Det synliggjør veien "
                "til resultatet og bidrar til å unngå misvisende mestertall fra"
                " én samlet sum.",
            ),
            example_title=t("Work through ADA LOVELACE", "Regn gjennom ADA LOVELACE"),
            example_body=t(
                "This is a teaching example of a name calculation, not a "
                "biographical reading. First add and reduce ADA, then LOVELACE."
                " Only then combine the two reduced parts.",
                "Dette er et øvingseksempel på en navneberegning, ikke en "
                "biografisk analyse. Summer og reduser først ADA, deretter "
                "LOVELACE. Legg så de to reduserte delene sammen.",
            ),
            formula="ADA: 6 · LOVELACE: 30 → 3 · 6 + 3 = 9",
            detail_title=t(
                "The name is not the birth date.", "Navnet er ikke fødselsdatoen."
            ),
            detail_body=t(
                "The expression number comes from the name. The life-path "
                "number comes from the birth date: reduce day, month and year "
                "separately, then combine them. The same final digit can "
                "therefore have a different role in the reading.",
                "Uttrykkstallet kommer fra navnet. Livsveistallet kommer fra "
                "fødselsdatoen: reduser dag, måned og år hver for seg, og legg "
                "dem deretter sammen. Det samme sluttsifferet kan derfor ha "
                "ulike roller i analysen.",
            ),
        ),
        "compute-life-path-number": dict(
            kind="method",
            image="personal",
            eyebrow=t("04 / Follow the birth date", "04 / Følg fødselsdatoen"),
            title=t("A date. A rhythm. A path.", "En dato. En rytme. En vei."),
            subtitle=t(
                "The headline number of a reading.", "Hovedtallet i en analyse."
            ),
            intro=t(
                "The life path number is derived from your full birth date. Åse"
                " treats it as the headline of a reading — the overall rhythm "
                "and the lessons a lifetime is built around.",
                "Livsveistallet beregnes fra hele fødselsdatoen din. Åse ser på "
                "det som overskriften i en analyse – den overordnede rytmen og "
                "lærdommene et liv bygges rundt.",
            ),
            alt=t(
                "Illustration of a personal journey through time",
                "Illustrasjon av en personlig reise gjennom tiden",
            ),
            section_title=t(
                "Day, month and year — one at a time.",
                "Dag, måned og år – én om gangen.",
            ),
            section_body=t(
                "Day, month and year are each reduced on their own before they "
                "are added together and reduced again — never as one long flat "
                "string of digits. That per-part reduction keeps a genuine "
                "master number (11, 22, 33) visible and prevents a false one "
                "from appearing.",
                "Dag, måned og år reduseres hver for seg før de legges sammen og"
                " reduseres på nytt – aldri som én lang rekke sifre. Denne "
                "delvise reduksjonen gjør at et ekte mestertall (11, 22, 33) "
                "blir synlig, og hindrer at et falskt dukker opp.",
            ),
            steps=[
                (
                    t("Write the date", "Skriv datoen"),
                    t(
                        "Use the full birth date: day, month and the four-digit"
                        " year.",
                        "Bruk hele fødselsdatoen: dag, måned og årstall med "
                        "fire sifre.",
                    ),
                ),
                (
                    t("Reduce the day", "Reduser dagen"),
                    t(
                        "Add the digits of the day until one digit remains, "
                        "retaining 11 and 22 when reached.",
                        "Legg sammen sifrene i dagen til ett siffer gjenstår, "
                        "og behold 11 og 22 når de oppstår.",
                    ),
                ),
                (
                    t("Reduce month and year", "Reduser måned og år"),
                    t(
                        "Treat the month and the year the same way, each as its"
                        " own part.",
                        "Behandle måneden og året på samme måte, hver som sin "
                        "egen del.",
                    ),
                ),
                (
                    t("Combine the parts", "Sett delene sammen"),
                    t(
                        "Add the three reduced parts, then apply the same "
                        "reduction rule to the total.",
                        "Legg sammen de tre reduserte delene, og bruk samme "
                        "reduksjonsregel på summen.",
                    ),
                ),
            ],
            example_title=t("Work through 29 July 1990", "Regn gjennom 29. juli 1990"),
            example_body=t(
                "This is a teaching example, not a personal reading. The day 29"
                " reduces to the master number 11, which is kept. July is 7. "
                "The year 1990 reduces to 1. Only then are the three parts "
                "combined.",
                "Dette er et øvingseksempel, ikke en personlig analyse. Dagen 29"
                " reduseres til mestertallet 11, som beholdes. Juli er 7. "
                "Året 1990 reduseres til 1. Først da legges de tre delene "
                "sammen.",
            ),
            formula="29 → 11 · 7 · 1990 → 1 · 11 + 7 + 1 = 19 → 1",
            detail_title=t(
                "The birth date is not the name.", "Fødselsdatoen er ikke navnet."
            ),
            detail_body=t(
                "The life path comes from the birth date and describes the "
                "rhythm of a lifetime. The destiny (expression) number comes "
                "from the name and describes the talents you develop. Compare "
                "the two to see where they align — or pull.",
                "Livsveistallet kommer fra fødselsdatoen og beskriver rytmen i "
                "et liv. Skjebnetallet (uttrykkstallet) kommer fra navnet og "
                "beskriver talentene du utvikler. Sammenlign de to for å se hvor"
                " de spiller sammen – eller trekker i hver sin retning.",
            ),
        ),
        "compute-name-vowel-consonant": dict(
            kind="method",
            image="calc-soul-urge",
            split_image="calc-personality",
            eyebrow=t("05 / Two voices in one name", "05 / To stemmer i ett navn"),
            title=t("Inner voice. Outer voice.", "Indre stemme. Ytre stemme."),
            subtitle=t(
                "Soul urge and personality.", "Sjelstall og personlighetstall."
            ),
            intro=t(
                "Your name holds two quieter numbers. The vowels give the soul "
                "urge number. The consonants give the personality number.",
                "Navnet ditt rommer to stillere tall. Vokalene gir sjelstallet. "
                "Konsonantene gir personlighetstallet.",
            ),
            alt=t(
                "Illustration of an open notebook with numbers on a desk",
                "Illustrasjon av en åpen notatbok med tall på et skrivebord",
            ),
            section_title=t("Split the letters.", "Del bokstavene."),
            section_body=t(
                "Vowels are the inner voice: what motivates you. Consonants "
                "are the outer voice: the first impression you give. Both use "
                "the same letter chart and the same per-part method.",
                "Vokalene er den indre stemmen: det som driver deg. "
                "Konsonantene er den ytre stemmen: førsteinntrykket du gir. "
                "Begge bruker samme bokstavtabell og samme metode, del for del.",
            ),
            pair=[
                dict(
                    id="soul-urge-number",
                    eyebrow=t("Vowels", "Vokaler"),
                    title=t("Soul urge number", "Sjelstallet"),
                    letters="A E I O U Y Æ Ø Å".split(),
                    body=t(
                        "What quietly motivates you — the needs beneath the "
                        "surface.",
                        "Det som driver deg i stillhet – behovene under "
                        "overflaten.",
                    ),
                ),
                dict(
                    id="personality-number",
                    eyebrow=t("Consonants", "Konsonanter"),
                    title=t("Personality number", "Personlighetstallet"),
                    letters="B C D F G H …".split(),
                    body=t(
                        "The first impression you make — the door others walk"
                        " through to meet you.",
                        "Førsteinntrykket du gir – døren andre går gjennom "
                        "for å møte deg.",
                    ),
                ),
            ],
            steps=[
                (
                    t("Write the name", "Skriv navnet"),
                    t(
                        "Keep first, middle and last names as separate parts.",
                        "Behold fornavn, mellomnavn og etternavn som egne deler.",
                    ),
                ),
                (
                    t("Sort the letters", "Sorter bokstavene"),
                    t(
                        "Vowels to one side, consonants to the other. Y, Æ, Ø "
                        "and Å count as vowels here.",
                        "Vokaler på én side, konsonanter på den andre. Y, Æ, Ø "
                        "og Å regnes som vokaler her.",
                    ),
                ),
                (
                    t("Reduce each part", "Reduser hver del"),
                    t(
                        "Add the values within each name part, then reduce. "
                        "Keep 11, 22 and 33.",
                        "Summer verdiene i hver navnedel, og reduser. Behold "
                        "11, 22 og 33.",
                    ),
                ),
                (
                    t("Combine the parts", "Sett delene sammen"),
                    t(
                        "Add the reduced parts and reduce once more.",
                        "Legg sammen de reduserte delene og reduser én gang til.",
                    ),
                ),
            ],
            example_title=t("Work through ANNA", "Regn gjennom ANNA"),
            example_body=t(
                "A teaching example. The vowels are A and A. The consonants are"
                " N and N.",
                "Et øvingseksempel. Vokalene er A og A. Konsonantene er N og N.",
            ),
            formula=t(
                "Vowels: 1 + 1 = 2 · Consonants: 5 + 5 = 10 → 1",
                "Vokaler: 1 + 1 = 2 · Konsonanter: 5 + 5 = 10 → 1",
            ),
            detail_title=t(
                "Two numbers from one submission.", "To tall fra én utregning."
            ),
            detail_body=t(
                "The calculator below returns both numbers at once — together "
                "with your life path and destiny numbers. Compare the inner and"
                " the outer voice: do they agree, or pull in different "
                "directions?",
                "Kalkulatoren under gir begge tallene samtidig – sammen med "
                "livsveistallet og skjebnetallet. Sammenlign den indre og den "
                "ytre stemmen: Er de enige, eller trekker de i hver sin "
                "retning?",
            ),
        ),
        "calculation-methods-overview": dict(
            kind="method",
            image="calc-methods",
            split_image="calc-methods",
            eyebrow=t("06 / The rules behind it all", "06 / Reglene bak alt"),
            title=t("How the numbers are reduced.", "Slik reduseres tallene."),
            subtitle=t(
                "One method. Used everywhere.", "Én metode. Brukt overalt."
            ),
            intro=t(
                "Every calculator on this site follows the same few rules. "
                "Learn them once — then every result can be checked by hand.",
                "Alle kalkulatorene her følger de samme få reglene. Lær dem én "
                "gang – så kan du etterprøve hvert resultat for hånd.",
            ),
            alt=t(
                "Illustration of old books and instruments in a library",
                "Illustrasjon av gamle bøker og instrumenter i et bibliotek",
            ),
            section_title=t(
                "Part by part, never one flat sum.",
                "Del for del, aldri én samlet sum.",
            ),
            section_body=t(
                "A flat sum of every letter or digit can land on a master "
                "number that isn't really there. Reducing each part first keeps"
                " the result honest.",
                "En samlet sum av alle bokstaver eller sifre kan gi et "
                "mestertall som egentlig ikke finnes. Reduserer du hver del "
                "først, blir resultatet ærlig.",
            ),
            steps=[
                (
                    t("Add the digits", "Summer sifrene"),
                    t(
                        "28 becomes 2 + 8 = 10, and 10 becomes 1 + 0 = 1.",
                        "28 blir 2 + 8 = 10, og 10 blir 1 + 0 = 1.",
                    ),
                ),
                (
                    t("Keep the master numbers", "Behold mestertallene"),
                    t(
                        "Stop at 11, 22 or 33 when you reach them. They also "
                        "carry 2, 4 and 6.",
                        "Stopp ved 11, 22 eller 33 når du når dem. De bærer "
                        "også 2, 4 og 6.",
                    ),
                ),
                (
                    t("Reduce each part first", "Reduser hver del først"),
                    t(
                        "Name parts — or day, month and year — are reduced on "
                        "their own before they are combined.",
                        "Navnedeler – eller dag, måned og år – reduseres hver "
                        "for seg før de legges sammen.",
                    ),
                ),
                (
                    t("Build on the core", "Bygg videre på kjernen"),
                    t(
                        "Personal years, months and days start from the same "
                        "reduced birth-date parts.",
                        "Personlige år, måneder og dager bygger på de samme "
                        "reduserte delene av fødselsdatoen.",
                    ),
                ),
            ],
            example_title=t("Work through OLA NILSEN", "Regn gjennom OLA NILSEN"),
            example_body=t(
                "A teaching example. Per part, OLA gives 10 → 1 and NILSEN "
                "gives 28 → 1. Together: 2. A flat sum of all letters would "
                "give 38 → 11 — a master number that isn't there.",
                "Et øvingseksempel. Del for del gir OLA 10 → 1 og NILSEN 28 → "
                "1. Sammen: 2. En samlet sum av alle bokstavene ville gitt 38 →"
                " 11 – et mestertall som ikke finnes.",
            ),
            formula="OLA 10 → 1 · NILSEN 28 → 1 · 1 + 1 = 2",
            detail_title=t(
                "Reproducible, then interpreted.", "Etterprøvbart, så tolket."
            ),
            detail_body=t(
                "The arithmetic can always be checked. What a number means is "
                "an interpretation — that part is where Åse's personal "
                "analysis begins.",
                "Regnestykket kan alltid etterprøves. Hva et tall betyr, er en "
                "tolkning – og det er der Åses personlige analyse begynner.",
            ),
        ),
        "pythagoras-legacy": dict(
            kind="history",
            image="pythagoras-portrait",
            eyebrow=t(
                "Ancient Greece / A philosophical foundation",
                "Antikkens Hellas / Et filosofisk utgangspunkt",
            ),
            title=t("Meet Pythagoras.", "Møt Pythagoras."),
            subtitle=t(
                "Number, music and the search for harmony.",
                "Tall, musikk og letingen etter harmoni.",
            ),
            intro=t(
                "Pythagoras lived around 570–490 BCE. The tradition associated "
                "with him made number and proportion central to thinking about "
                "an ordered world.",
                "Pythagoras levde omkring 570–490 f.Kr. Tradisjonen som knyttes"
                " til ham, gjorde tall og proporsjoner sentrale i tenkningen om"
                " en ordnet verden.",
            ),
            alt=t(
                "Imagined historical portrait of Pythagoras with a monochord in"
                " a Greek colonnade",
                "Historisk inspirert portrett av Pythagoras med et monokord "
                "mellom greske søyler",
            ),
            section_title=t(
                "A person, a school, a long afterlife.",
                "Et menneske, en skole, en lang etterhistorie.",
            ),
            section_body=t(
                "Pythagoras left no writings. Much of what we know comes from "
                "later accounts, and the work of his followers must be "
                "distinguished from claims about the man himself. The portrait "
                "is an artistic interpretation, not a verified likeness.",
                "Pythagoras etterlot seg ingen skrifter. Mye av det vi vet, "
                "kommer fra senere beretninger, og tilhengernes arbeid må "
                "skilles fra påstander om personen selv. Portrettet er en "
                "kunstnerisk tolkning, ikke en dokumentert avbildning.",
            ),
            example_title=t("Listen to a ratio.", "Lytt til et forhold."),
            example_body=t(
                "Musical intervals can be described by numerical ratios. An "
                "octave corresponds to a frequency ratio of 2:1. Such "
                "relationships help explain why harmony became a powerful image"
                " of numerical order.",
                "Musikalske intervaller kan beskrives med tallforhold. En oktav"
                " har frekvensforholdet 2:1. Slike sammenhenger bidrar til å "
                "forklare hvorfor harmoni ble et sterkt bilde på orden uttrykt "
                "med tall.",
            ),
            formula="2 : 1",
            detail_title=t(
                "Inspiration is not the same as invention.",
                "Inspirasjon er ikke det samme som oppfinnelse.",
            ),
            detail_body=t(
                "Modern numerology draws inspiration from Pythagorean number "
                "symbolism. That does not establish that Pythagoras invented "
                "today’s alphabet tables or personal name readings. Åse’s "
                "practice belongs to the modern interpretive tradition.",
                "Moderne numerologi henter inspirasjon fra pytagoreisk "
                "tallsymbolikk. Det fastslår ikke at Pythagoras oppfant dagens "
                "alfabet-tabeller eller personlige navneanalyser. Åses praksis "
                "hører til den moderne tolkningstradisjonen.",
            ),
        ),
    }
    lesson = {**common, **pages[slug]}
    themes = [
        (
            1,
            "Initiative",
            "Initiativ",
            "Begin something meaningful.",
            "Begynn på noe meningsfullt.",
            "Independence and listening.",
            "Selvstendighet og lytting.",
        ),
        (
            2,
            "Cooperation",
            "Samarbeid",
            "Listen and build trust.",
            "Lytt og bygg tillit.",
            "Sensitivity and boundaries.",
            "Følsomhet og grenser.",
        ),
        (
            3,
            "Expression",
            "Uttrykk",
            "Give an idea a voice.",
            "Gi en idé en stemme.",
            "Creativity and follow-through.",
            "Kreativitet og gjennomføring.",
        ),
        (
            4,
            "Structure",
            "Struktur",
            "Build a steady foundation.",
            "Bygg et stødig fundament.",
            "Reliability and flexibility.",
            "Pålitelighet og fleksibilitet.",
        ),
        (
            5,
            "Freedom",
            "Frihet",
            "Explore a new perspective.",
            "Utforsk et nytt perspektiv.",
            "Variety and commitment.",
            "Variasjon og forpliktelse.",
        ),
        (
            6,
            "Care",
            "Omsorg",
            "Make room for care.",
            "Gi omsorgen plass.",
            "Responsibility and self-care.",
            "Ansvar og egenomsorg.",
        ),
        (
            7,
            "Reflection",
            "Fordypning",
            "Ask a deeper question.",
            "Still et dypere spørsmål.",
            "Solitude and connection.",
            "Alenetid og fellesskap.",
        ),
        (
            8,
            "Realisation",
            "Realisering",
            "Turn intention into action.",
            "Gjør intensjon til handling.",
            "Ambition and integrity.",
            "Ambisjoner og integritet.",
        ),
        (
            9,
            "Completion",
            "Fullføring",
            "See the bigger picture.",
            "Se den større sammenhengen.",
            "Compassion and letting go.",
            "Medfølelse og å gi slipp.",
        ),
    ]
    lesson["numbers"] = [
        dict(number=n, title=t(en, nb), invitation=t(a, b), balance=t(c, d))
        for n, en, nb, a, b, c, d in themes
    ]
    lesson["chart"] = [
        dict(value=n, letters=" · ".join(k for k, v in LETTER_VALUES.items() if v == n))
        for n in range(1, 10)
    ]
    # Transposed for the compact 1–9 grid: one column per value, letters
    # stacked beneath (Å, Æ and Ø make some columns one row taller).
    columns = [[k for k, v in LETTER_VALUES.items() if v == n] for n in range(1, 10)]
    lesson["chart_rows"] = [
        [col[i] if i < len(col) else "" for col in columns]
        for i in range(max(len(col) for col in columns))
    ]
    lesson.setdefault("steps", [
        (
            t("Write the name", "Skriv navnet"),
            t(
                "Keep first, middle and last names as separate parts. Use the "
                "name agreed for the reading.",
                "Behold fornavn, mellomnavn og etternavn som separate deler. "
                "Bruk navnet som er avtalt for analysen.",
            ),
        ),
        (
            t("Look up and add", "Slå opp og summer"),
            t(
                "Convert each letter using the chart. Add the letters within "
                "each name part.",
                "Gjør hver bokstav om til en tallverdi. Summer bokstavene "
                "innenfor hver navnedel.",
            ),
        ),
        (
            t("Reduce each part", "Reduser hver del"),
            t(
                "Add the digits until one digit remains, retaining 11, 22 and "
                "33 when reached.",
                "Legg sammen sifrene til ett siffer gjenstår, og behold 11, 22 "
                "og 33 når de oppstår.",
            ),
        ),
        (
            t("Combine the parts", "Sett delene sammen"),
            t(
                "Add the reduced name parts, then apply the same reduction rule"
                " to the total.",
                "Legg sammen de reduserte navnedelene, og bruk samme "
                "reduksjonsregel på summen.",
            ),
        ),
    ])
    lesson["related"] = [
        (s, "/" + s + "/", p["title"])
        for s, p in pages.items()
        if s != slug and p["kind"] != "history"
    ]
    return lesson


def ase_content(language):
    no = language in ("nb", "no", "nn")

    def t(en, nb):
        return nb if no else en

    return dict(
        eyebrow=t("Your guide", "Din veileder"),
        title="Åse Karin Steinsland",
        body=t(
            "Numerologist and life guide near Bergen. Personal analyses since"
            " 1997.",
            "Numerolog og livsveileder ved Bergen. Personlige analyser siden "
            "1997.",
        ),
        method=t(
            "“Calculate the parts. Then read the whole.”",
            "«Beregn delene. Les deretter helheten.»",
        ),
        link=t("Meet Åse", "Møt Åse"),
        method_link=t("Learn the method", "Lær metoden"),
        since=t("Since 1997", "Siden 1997"),
    )
