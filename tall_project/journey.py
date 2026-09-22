"""Bilingual editorial content for the history of numbers."""


def journey_content(language):
    no = language in ("nb", "no", "nn")

    def t(en, nb):
        return nb if no else en

    chapters = [
        dict(
            id="mesopotamia",
            numeral="02",
            date=t("c. 3300 BCE · Mesopotamia", "ca. 3300 f.Kr. · Mesopotamia"),
            label=t("Recording the world", "Å registrere verden"),
            title=t("When counting became writing.", "Da telling ble til skrift."),
            body=t(
                "A harvest. A flock. A trade. In the cities of Mesopotamia, clay "
                "tokens and tablets helped people record what they owned and "
                "exchanged. Numbers made everyday life visible — and helped shape "
                "the beginnings of writing.",
                "En avling. En flokk. En handel. I Mesopotamias byer hjalp "
                "leirbrikker og tavler mennesker med å registrere det de eide og "
                "byttet. Tall gjorde hverdagen oversiktlig og bidro til skriftens "
                "begynnelse.",
            ),
            note=t(
                "This is the history of counting and record keeping, not evidence "
                "of modern numerology.",
                "Dette er historien om telling og registrering, ikke dokumentasjon"
                " på moderne numerologi.",
            ),
            alt=t(
                "Illustrated clay tablet and counting tokens overlooking an "
                "ancient city",
                "Illustrert leirtavle og tellebrikker med en oldtidsby i bakgrunnen",
            ),
            symbol="tablet",
            source="https://www.metmuseum.org/art/collection/search/325500",
            source_name="The Metropolitan Museum of Art",
        ),
        dict(
            id="pythagoras",
            numeral="03",
            date=t(
                "6th–5th century BCE · Ancient Greece",
                "500–400-tallet f.Kr. · Antikkens Hellas",
            ),
            label=t("Seeking harmony", "På leting etter harmoni"),
            title=t("Could numbers explain the cosmos?", "Kunne tall forklare kosmos?"),
            body=t(
                "The Pythagorean tradition connected number, proportion and the "
                "order of the world. Musical intervals offered a striking example "
                "of relationships expressed through ratios. Number became a way to"
                " think about harmony, as well as quantity.",
                "Den pytagoreiske tradisjonen knyttet tall og proporsjoner til "
                "verdens orden. Musikalske intervaller ga et tydelig eksempel på "
                "forhold som kunne uttrykkes med tall. Tall ble en måte å tenke om"
                " harmoni på, i tillegg til mengde.",
            ),
            note=t(
                "Pythagoras left no writings. Later accounts mix history and "
                "legend; today’s name charts should not be presented as his "
                "documented invention.",
                "Pythagoras etterlot seg ingen skrifter. Senere beretninger "
                "blander historie og legende; dagens navnetabeller bør ikke "
                "fremstilles som hans dokumenterte oppfinnelse.",
            ),
            alt=t(
                "Artistic reconstruction of a Greek colonnade, monochord and "
                "triangular pebble arrangement",
                "Kunstnerisk rekonstruksjon av greske søyler, monokord og småstein"
                " i trekant",
            ),
            symbol="triangle",
            source="https://plato.stanford.edu/entries/pythagoras/",
            source_name="Stanford Encyclopedia of Philosophy",
            link="/pythagoras-legacy/",
            link_label=t(
                "Explore the Pythagorean tradition",
                "Utforsk den pytagoreiske tradisjonen",
            ),
        ),
        dict(
            id="traditions",
            numeral="04",
            date=t(
                "Across centuries · Across cultures",
                "Gjennom århundrer · På tvers av kulturer",
            ),
            label=t("Numbers become symbols", "Tall blir symboler"),
            title=t(
                "Many traditions. Many meanings.",
                "Mange tradisjoner. Mange betydninger.",
            ),
            body=t(
                "Numbers also became a language for ideas: unity, balance, "
                "completeness and renewal. Religious texts, philosophy and "
                "literature gave them different meanings in different settings. "
                "These traditions do not form one universal code — their context "
                "matters.",
                "Tall ble også et språk for ideer: enhet, balanse, helhet og "
                "fornyelse. Religiøse tekster, filosofi og litteratur ga dem ulike"
                " betydninger i ulike sammenhenger. Tradisjonene utgjør ikke én "
                "universell kode – sammenhengen er viktig.",
            ),
            note=t(
                "Symbolic interpretation varies between cultures and schools. A "
                "shared number does not necessarily mean a shared belief.",
                "Symbolske tolkninger varierer mellom kulturer og retninger. Et "
                "felles tall betyr ikke nødvendigvis en felles tro.",
            ),
            alt=t(
                "Imagined historical library with manuscripts and a brass "
                "armillary sphere",
                "Illustrert historisk bibliotek med manuskripter og en "
                "armillarsfære i messing",
            ),
            symbol="book",
        ),
        dict(
            id="modern",
            numeral="05",
            date=t(
                "Modern practice · 20th century onward",
                "Moderne praksis · Fra 1900-tallet",
            ),
            label=t(
                "From symbols to self-reflection", "Fra symboler til selvrefleksjon"
            ),
            title=t(
                "A more personal reading of numbers.",
                "En mer personlig lesning av tall.",
            ),
            body=t(
                "Modern numerology turns attention toward names and birth dates. "
                "Practitioners assign letter values, add digits and interpret the "
                "resulting numbers through their chosen system. Different schools "
                "use different conventions, including how they handle master "
                "numbers.",
                "Moderne numerologi retter oppmerksomheten mot navn og "
                "fødselsdatoer. Utøvere gir bokstaver tallverdier, summerer sifre "
                "og tolker resultatene innenfor sitt valgte system. Retningene "
                "bruker ulike regler, blant annet for hvordan mestertall "
                "behandles.",
            ),
            note=t(
                "Numerology is a symbolic practice for reflection; it is not a "
                "scientifically validated method of predicting personality or "
                "future events.",
                "Numerologi er en symbolsk praksis for refleksjon. Det er ikke en "
                "vitenskapelig validert metode for å forutsi personlighet eller "
                "fremtidige hendelser.",
            ),
            alt=t(
                "Illustrated vintage desk with notebook, number charts and "
                "fountain pen",
                "Illustrert skrivebord med notatbok, talltabeller og fyllepenn",
            ),
            symbol="grid",
            link="/calculation-methods-overview/",
            link_label=t(
                "See how the calculations work", "Se hvordan beregningene fungerer"
            ),
        ),
        dict(
            id="personal",
            numeral="06",
            date=t("Today · Your next chapter", "I dag · Ditt neste kapittel"),
            label=t("From history to your story", "Fra historien til din historie"),
            title=t("What do you see in your numbers?", "Hva ser du i dine tall?"),
            body=t(
                "Here, Åse Steinsland’s approach brings numerical calculations "
                "together with personal interpretation. Start with the method, "
                "explore the meanings, and use the questions that resonate with "
                "you as a starting point for reflection.",
                "Her kombinerer Åse Steinslands tilnærming numeriske beregninger "
                "med personlig tolkning. Begynn med metoden, utforsk betydningene "
                "og bruk spørsmålene som treffer deg som et utgangspunkt for "
                "refleksjon.",
            ),
            note=t(
                "The calculation follows a rule. The meaning is an interpretation."
                " Your choices remain your own.",
                "Beregningen følger en regel. Betydningen er en tolkning. Valgene "
                "er fortsatt dine.",
            ),
            alt=t(
                "Illustrated contemporary Scandinavian desk beside a Norwegian fjord",
                "Illustrert moderne skandinavisk skrivebord ved en norsk fjord",
            ),
            symbol="spark",
            link="/calculators/",
            link_label=t("Explore your numbers", "Utforsk dine tall"),
        ),
    ]
    labels = dict(
        eyebrow=t("DISCOVER NUMEROLOGY", "OPPDAG NUMEROLOGI"),
        title=t("Every number.", "Hvert tall."),
        title_em=t("A story.", "En historie."),
        intro=t(
            "From the first marks we made to the meanings we find today. "
            "Follow the human fascination with numbers — across time, cultures"
            " and your own life.",
            "Fra de første strekene vi risset til betydningen vi finner i dag."
            " Følg menneskets fascinasjon for tall – gjennom tid, kulturer og "
            "ditt eget liv.",
        ),
        start=t("Begin the journey", "Start reisen"),
        chapter=t("Chapter", "Kapittel"),
        hero_date=t("01 / Before written history", "01 / Før den skrevne historien"),
        hero_caption=t(
            "Before numbers had names, the world had patterns.",
            "Før tallene fikk navn, hadde verden mønstre.",
        ),
        hero_alt=t(
            "Artistic prehistoric coastline with stars, grouped stones and a "
            "tally stick",
            "Kunstnerisk kystlandskap fra forhistorisk tid med stjerner, "
            "grupperte steiner og en tellestav",
        ),
        nav=t("Chapters in the journey", "Kapitler i reisen"),
        origins=t("Beginnings", "Begynnelsen"),
        nav_labels=[
            t("Clay", "Leire"),
            t("Harmony", "Harmoni"),
            t("Symbols", "Symboler"),
            t("Names", "Navn"),
            t("You", "Deg"),
        ],
        bridge_title=t(
            "First we counted. Then we wondered.", "Først telte vi. Så undret vi oss."
        ),
        bridge=t(
            "Days and seasons. People and possessions. The history of numbers "
            "begins with practical questions, while the search for their "
            "deeper meaning follows many different paths.",
            "Dager og årstider. Mennesker og eiendeler. Tallenes historie "
            "begynner med praktiske spørsmål, mens letingen etter dypere "
            "mening følger mange forskjellige veier.",
        ),
        read_source=t("Historical source", "Historisk kilde"),
        art_note=t(
            "Original artistic illustrations. Historical scenes are "
            "interpretations, not photographs of verified artifacts.",
            "Originale kunstneriske illustrasjoner. Historiske scener er "
            "tolkninger, ikke fotografier av dokumenterte gjenstander.",
        ),
        next=t("Keep exploring", "Utforsk videre"),
        references=t("Sources & perspective", "Kilder og perspektiv"),
        references_text=t(
            "The early-history sections draw on museum scholarship and the "
            "Stanford Encyclopedia of Philosophy. Modern numerology is "
            "presented as an interpretive tradition, separate from the history"
            " of mathematics.",
            "Delene om tidlig historie bygger på museumsfaglige kilder og "
            "Stanford Encyclopedia of Philosophy. Moderne numerologi "
            "presenteres som en tolkningstradisjon, adskilt fra matematikkens "
            "historie.",
        ),
        faq=t("A few questions along the way", "Noen spørsmål på veien"),
        pause=t("Pause motion", "Stopp bevegelse"),
        resume=t("Enable motion", "Aktiver bevegelse"),
    )
    resources = [
        (
            "/general-interpretation/",
            t("The language of numbers", "Tallenes språk"),
            t(
                "Explore the symbolic meanings of the core numbers.",
                "Utforsk de symbolske betydningene til grunntallene.",
            ),
            "spark",
        ),
        (
            "/letter-value-chart/",
            t("From letters to numbers", "Fra bokstaver til tall"),
            t(
                "See the letter values used in a reading.",
                "Se bokstavverdiene som brukes i en lesning.",
            ),
            "grid",
        ),
        (
            "/compute-destiny-number/",
            t("Follow a calculation", "Følg en beregning"),
            t(
                "Understand the steps behind a personal number.",
                "Forstå stegene bak et personlig tall.",
            ),
            "triangle",
        ),
    ]
    faqs = [
        (
            t(
                "Is numerology the same as astrology?",
                "Er numerologi det samme som astrologi?",
            ),
            t(
                "No. Numerology interprets numbers derived from names and dates; "
                "astrology interprets celestial positions. Some practitioners "
                "combine them, but they are different systems.",
                "Nei. Numerologi tolker tall fra navn og datoer; astrologi tolker "
                "himmellegemenes posisjoner. Noen utøvere kombinerer dem, men de "
                "er forskjellige systemer.",
            ),
        ),
        (
            t(
                "Did Pythagoras invent modern numerology?",
                "Oppfant Pythagoras moderne numerologi?",
            ),
            t(
                "Modern systems often draw inspiration from Pythagorean ideas. "
                "That is different from establishing that Pythagoras invented "
                "today’s letter charts or personal readings.",
                "Moderne systemer henter ofte inspirasjon fra pytagoreiske ideer. "
                "Det er noe annet enn å fastslå at Pythagoras oppfant dagens "
                "bokstavtabeller eller personlige lesninger.",
            ),
        ),
        (
            t("Where can I begin?", "Hvor kan jeg begynne?"),
            t(
                "Follow the calculation guide or explore the calculator suite. "
                "Read which rules are being used before comparing results between "
                "different systems.",
                "Følg beregningsveiledningen eller utforsk kalkulatorene. Les "
                "hvilke regler som brukes før du sammenligner resultater fra ulike"
                " systemer.",
            ),
        ),
    ]
    return dict(chapters=chapters, labels=labels, resources=resources, faqs=faqs)
