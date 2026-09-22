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
    lesson["steps"] = [
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
    ]
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
        eyebrow=t(
            "Your guide / Åse Karin Steinsland", "Din veileder / Åse Karin Steinsland"
        ),
        title=t(
            "Years of practice. A personal approach.",
            "Mange års praksis. En personlig tilnærming.",
        ),
        body=t(
            "Åse is a numerologist and life guide based outside Bergen. She"
            " has created personal numerology analyses since 1997. Her work"
            " brings a Pythagorean-inspired calculation method together "
            "with a conversation about the person behind the numbers.",
            "Åse er numerolog og livsveileder, bosatt utenfor Bergen. Hun "
            "har laget personlige numerologiske analyser siden 1997. "
            "Arbeidet hennes kombinerer en pytagoreisk inspirert "
            "beregningsmetode med en samtale om mennesket bak tallene.",
        ),
        method=t(
            "Calculate the parts. Then read the whole.",
            "Beregn delene. Les deretter helheten.",
        ),
        explanation=t(
            "Names are calculated part by part; day, month and year are "
            "also treated separately. The number is a starting point for "
            "interpretation. The website’s automatic calculation is "
            "distinct from Åse’s personal analysis and guidance.",
            "Navn beregnes del for del; dag, måned og år behandles også "
            "separat. Tallet er et utgangspunkt for tolkning. Nettstedets "
            "automatiske beregning er noe annet enn Åses personlige analyse"
            " og veiledning.",
        ),
        link=t("Meet Åse", "Møt Åse"),
        method_link=t("Learn the method", "Lær metoden"),
        since=t("Personal analyses since 1997", "Personlige analyser siden 1997"),
    )
