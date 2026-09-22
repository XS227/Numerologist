"""Bilingual editorial content for the WOW-signal / Arecibo Line article.

Same pattern as tall_project/journey.py (the Discover Numerology redesign):
a hero + N chapters, rendered by articles/templates/articles/detail_wow_signal.html
reusing the shared journey.css/journey.js design system.

Every date/vibration figure here was independently verified against the
source research note (Arecibo-Line/Numerisk_og_astronomisk_sammenheng.md)
before writing — that note had real errors (1977 given as vibration 5,
actually 6; 2012 given as 6, actually 5; the Arecibo-to-Wow! gap claimed
as 9797 days, actually 1003). None of the wrong figures are used here.
The ATLAS comet's claimed overlap with the Wow! signal region is left as
an open question, not asserted as fact — see the "atlas" chapter's note.
"""


def wow_journey_content(language):
    no = language in ("nb", "no", "nn")

    def t(en, nb):
        return nb if no else en

    chapters = [
        dict(
            id="arecibo",
            numeral="02",
            date=t("16 Nov 1974 · Arecibo Observatory", "16. november 1974 · Arecibo-observatoriet"),
            label=t("The transmission", "Sendingen"),
            title=t("A message written in numbers.", "Et budskap skrevet i tall."),
            body=t(
                "On 16 November 1974, Arecibo Observatory beamed a binary "
                "message toward the globular cluster M13 — numbers, DNA, a "
                "stick figure, meant to outlast everyone who sent it. "
                "Reduced by day, month and year: 16 → 7, 11 → 2, 1974 → 3. "
                "Together: 7 + 2 + 3 = 12 → 3, the number of communication "
                "and expression.",
                "16. november 1974 sendte Arecibo-observatoriet en binær "
                "melding mot kulehopen M13 – tall, DNA, en menneskefigur, "
                "ment å vare lenger enn noen av oss. Redusert etter dag, "
                "måned og år: 16 → 7, 11 → 2, 1974 → 3. Sammen: 7 + 2 + 3 = "
                "12 → 3, kommunikasjonens og uttrykkets tall.",
            ),
            note=t(
                "This is a numerological reading of a real, documented "
                "transmission — not a claim about its scientific content.",
                "Dette er en numerologisk lesning av en reell, dokumentert "
                "sending – ikke en påstand om dens vitenskapelige innhold.",
            ),
            alt=t(
                "Illustrated radio telescope dish transmitting a beam of "
                "light into a starry night sky",
                "Illustrert radioteleskop som sender en lysstråle mot en "
                "stjernehimmel",
            ),
            symbol="dish",
        ),
        dict(
            id="wow",
            numeral="03",
            date=t("15 Aug 1977 · Big Ear Observatory, Ohio", "15. august 1977 · Big Ear-observatoriet, Ohio"),
            label=t("The reply", "Svaret"),
            title=t("72 seconds no one has explained.", "72 sekunder ingen har forklart."),
            body=t(
                "Less than three years later, the Big Ear radio telescope "
                "recorded a signal so strong astronomer Jerry Ehman circled "
                "the printout and wrote one word: “Wow!”. Reduced: day 15 → "
                "6, month 8 → 8, year 1977 → 6. Together: 6 + 8 + 6 = 20 → "
                "2 — reception and balance, where Arecibo's 3 was outward "
                "expression.",
                "Under tre år senere fanget Big Ear-radioteleskopet opp et "
                "signal så sterkt at astronomen Jerry Ehman sirklet "
                "utskriften og skrev ett ord: «Wow!». Redusert: dag 15 → 6, "
                "måned 8 → 8, år 1977 → 6. Sammen: 6 + 8 + 6 = 20 → 2 – "
                "mottak og balanse, der Arecibos 3 var utadvendt uttrykk.",
            ),
            note=t(
                "The signal's origin has never been identified. Numerology "
                "offers a lens on the dates, not an explanation for the "
                "signal itself.",
                "Signalets opprinnelse er aldri identifisert. Numerologien "
                "tilbyr en lesning av datoene, ikke en forklaring på selve "
                "signalet.",
            ),
            alt=t(
                "Illustrated observatory desk with a paper printout marked "
                "in the margin, night sky through a window",
                "Illustrert observatorie-skrivebord med en utskrift merket "
                "i margen, stjernehimmel gjennom et vindu",
            ),
            symbol="wave",
        ),
        dict(
            id="interval",
            numeral="04",
            date=t("1,003 days", "1003 dager"),
            label=t("The gap", "Mellomrommet"),
            title=t("From sending to hearing back.", "Fra sending til svar."),
            body=t(
                "Exactly 1,003 days separate the Arecibo message from the "
                "Wow! signal. Digit-reduced: 1 + 0 + 0 + 3 = 4 — the "
                "builder's number, structure and foundation. Between a "
                "message sent in the spirit of 3 and a signal received in "
                "the spirit of 2 lies a 4's distance: not a dramatic span, "
                "but a grounded one.",
                "Nøyaktig 1003 dager skiller Arecibo-meldingen fra "
                "WOW!-signalet. Kvertsifret: 1 + 0 + 0 + 3 = 4 – byggerens "
                "tall, struktur og fundament. Mellom en melding sendt i "
                "treerens ånd og et signal mottatt i toerens, ligger det "
                "en fireners avstand: ikke en dramatisk periode, men en "
                "jordnær en.",
            ),
            note=t(
                "1,003 is the actual, verified gap — an earlier draft of "
                "this research note misstated it as 9,797 days.",
                "1003 er den faktiske, verifiserte avstanden – et "
                "tidligere utkast av dette forskningsnotatet oppga "
                "feilaktig 9797 dager.",
            ),
            alt=t(
                "Illustrated night sky with long star trails suggesting "
                "the passage of time",
                "Illustrert stjernehimmel med lange stjernespor som "
                "antyder tidens gang",
            ),
            symbol="trail",
        ),
        dict(
            id="frb",
            numeral="05",
            date=t("2 Nov 2012 · Arecibo Observatory", "2. november 2012 · Arecibo-observatoriet"),
            label=t("The echo", "Ekkoet"),
            title=t("A signal that repeats itself.", "Signalet som gjentar seg."),
            body=t(
                "On 2 November 2012, the very observatory that sent the "
                "1974 message detected a radio source far beyond the Milky "
                "Way, later named FRB 121102 — the first fast radio burst "
                "ever confirmed to repeat. Reduced: day 2 → 2, month 11 → "
                "2, year 2012 → 5. Together: 2 + 2 + 5 = 9, completion and "
                "repetition — fitting for a source whose defining trait is "
                "recurrence. The catalogue name itself, 121102, reduces to "
                "7: the seeker's number.",
                "2. november 2012 oppdaget nettopp observatoriet som sendte "
                "meldingen i 1974 en radiokilde langt utenfor Melkeveien, "
                "senere kalt FRB 121102 – det første fast radioutbruddet "
                "som noen gang er bekreftet å gjenta seg. Redusert: dag 2 → "
                "2, måned 11 → 2, år 2012 → 5. Sammen: 2 + 2 + 5 = 9, "
                "fullendelse og gjentakelse – passende for en kilde hvis "
                "kjennetegn nettopp er å gjenta seg. Selve "
                "katalogbetegnelsen 121102 reduseres til 7: søkerens tall.",
            ),
            note=t(
                "That the same observatory sent the 1974 message and later "
                "detected this repeating source is a documented fact, "
                "independent of the numerology.",
                "At det samme observatoriet sendte meldingen i 1974 og "
                "senere fanget opp denne gjentakende kilden, er et "
                "dokumentert faktum, uavhengig av numerologien.",
            ),
            alt=t(
                "Illustrated deep space scene with a distant nebula and "
                "rhythmic pulses of light",
                "Illustrert dypt rom-scene med en fjern tåke og "
                "rytmiske lysglimt",
            ),
            symbol="pulse",
        ),
        dict(
            id="atlas",
            numeral="06",
            date=t("Discovered December 2019", "Oppdaget desember 2019"),
            label=t("The open question", "Det åpne spørsmålet"),
            title=t("Did a comet cross the same field?", "Krysset en komet samme himmelfelt?"),
            body=t(
                "The Arecibo Line project's working notes ask whether "
                "comet C/2019 Y4 (ATLAS) passed through the same patch of "
                "sky the Wow! signal came from. It's a genuinely "
                "interesting question — but the notes themselves call the "
                "calculation preliminary, and there isn't enough verified "
                "work here yet to say anything definite.",
                "Arecibo Line-prosjektets arbeidsnotater spør om kometen "
                "C/2019 Y4 (ATLAS) passerte gjennom det samme himmelfeltet "
                "WOW!-signalet kom fra. Det er et genuint interessant "
                "spørsmål – men notatene selv kaller beregningen "
                "foreløpig, og det finnes ikke nok verifisert arbeid her "
                "ennå til å si noe sikkert.",
            ),
            note=t(
                "Left open deliberately: no coordinates or reduced numbers "
                "are asserted here that this project could not verify.",
                "Holdt bevisst åpent: ingen koordinater eller reduserte "
                "tall påstås her som dette prosjektet ikke kunne "
                "verifisere.",
            ),
            alt=t(
                "Illustrated comet streaking across a dark night sky above "
                "a horizon",
                "Illustrert komet som stryker over en mørk nattehimmel "
                "over en horisont",
            ),
            symbol="comet",
        ),
        dict(
            id="reflection",
            numeral="07",
            date=t("Today", "I dag"),
            label=t("The reflection", "Refleksjonen"),
            title=t("Numbers, not proof.", "Tall, ikke bevis."),
            body=t(
                "Nothing here proves the Arecibo message and the Wow! "
                "signal are physically connected — they're separated by "
                "light-years and coincidences no one controls. What "
                "numerology offers is a language for the wondering itself: "
                "a message sent in the spirit of 3, a signal received in "
                "the spirit of 2, and a builder's 4 between them — a "
                "pattern worth sitting with, not a verdict. The Arecibo "
                "Line project keeps gathering more events like these; this "
                "is one step, not a final answer.",
                "Ingenting her beviser at Arecibo-meldingen og "
                "WOW!-signalet henger sammen i noen fysisk forstand – de "
                "er adskilt av lysår og tilfeldigheter ingen kontrollerer. "
                "Det numerologien tilbyr er et språk for undringen selv: "
                "en melding sendt i treerens ånd, et signal mottatt i "
                "toerens, og en byggende firer mellom dem – et mønster "
                "verdt å sitte med, ikke en dom. Arecibo Line-prosjektet "
                "fortsetter å samle flere slike hendelser; dette er ett "
                "skritt, ikke et endelig svar.",
            ),
            note=t(
                "Numerology here is a reflective lens, not a scientific "
                "claim about radio astronomy.",
                "Numerologien her er en reflekterende linse, ikke en "
                "vitenskapelig påstand om radioastronomi.",
            ),
            alt=t(
                "Illustrated open observatory dome at night, quiet and "
                "facing the stars",
                "Illustrert åpen observatoriekuppel om natten, stille og "
                "vendt mot stjernene",
            ),
            symbol="spark",
        ),
    ]
    labels = dict(
        eyebrow=t("ARECIBO LINE", "ARECIBO LINE"),
        title=t("A message.", "En melding."),
        title_em=t("An echo.", "Et ekko."),
        intro=t(
            "In 1974 humanity sent a message to the stars. Three years "
            "later, something answered — or seemed to. This is a "
            "numerological reading of the dates between them, not a claim "
            "about what the Wow! signal was.",
            "I 1974 sendte menneskeheten en melding til stjernene. Tre år "
            "senere svarte noe – eller så virket det slik. Dette er en "
            "numerologisk lesning av datoene mellom dem, ikke en påstand "
            "om hva WOW!-signalet var.",
        ),
        start=t("Begin the reading", "Start lesningen"),
        chapter=t("Chapter", "Kapittel"),
        hero_date=t("01 / 16 November 1974", "01 / 16. november 1974"),
        hero_caption=t(
            "Before the reply came, we sent the first word.",
            "Før svaret kom, sendte vi det første ordet.",
        ),
        hero_alt=t(
            "Illustrated radio telescope dish under a night sky filled "
            "with stars",
            "Illustrert radioteleskop under en stjernefylt nattehimmel",
        ),
        nav=t("Chapters in this reading", "Kapitler i denne lesningen"),
        origins=t("The signal", "Signalet"),
        bridge_title=t(
            "First we spoke. Then we listened.",
            "Først talte vi. Så lyttet vi.",
        ),
        bridge=t(
            "A transmission, a reply, a gap between them, an echo 38 years "
            "later, and one open question. Five real events, read through "
            "the same numerology this whole site uses.",
            "En sending, et svar, et mellomrom, et ekko 38 år senere, og "
            "ett åpent spørsmål. Fem virkelige hendelser, lest gjennom "
            "samme numerologi som resten av dette nettstedet bruker.",
        ),
        read_source=t("Source", "Kilde"),
        art_note=t(
            "Original artistic illustrations. Historical scenes are "
            "interpretations, not photographs of the actual events.",
            "Originale kunstneriske illustrasjoner. Historiske scener er "
            "tolkninger, ikke fotografier av de faktiske hendelsene.",
        ),
        next=t("Keep exploring", "Utforsk videre"),
        references=t("Sources & perspective", "Kilder og perspektiv"),
        references_text=t(
            "The dates and events here are documented history (Arecibo "
            "Observatory, the Big Ear Observatory, and FRB 121102's "
            "discovery record). The numerology is presented as a "
            "reflective, interpretive reading — not a scientific claim "
            "about any of them.",
            "Datoene og hendelsene her er dokumentert historie "
            "(Arecibo-observatoriet, Big Ear-observatoriet og "
            "oppdagelsen av FRB 121102). Numerologien presenteres som en "
            "reflekterende, tolkende lesning – ikke en vitenskapelig "
            "påstand om noen av dem.",
        ),
        faq=t("A few questions along the way", "Noen spørsmål på veien"),
        pause=t("Pause motion", "Stopp bevegelse"),
        resume=t("Enable motion", "Aktiver bevegelse"),
    )
    resources = [
        (
            "/articles/hva-avslorer-tallene-i-shahnameh/",
            t("Numbers in the Shahnameh", "Tallene i Shahnameh"),
            t(
                "Another numerological reading of real historical figures.",
                "En annen numerologisk lesning av reelle historiske tall.",
            ),
            "book",
        ),
        (
            "/calculators/",
            t("Try the calculator", "Prøv kalkulatoren"),
            t(
                "Reduce your own dates the same way, step by step.",
                "Reduser dine egne datoer på samme måte, steg for steg.",
            ),
            "grid",
        ),
        (
            "/calculation-methods-overview/",
            t("How the reduction works", "Hvordan reduksjonen fungerer"),
            t(
                "The method behind every number on this page.",
                "Metoden bak hvert tall på denne siden.",
            ),
            "triangle",
        ),
    ]
    faqs = [
        (
            t("Is any of this scientifically proven?", "Er noe av dette vitenskapelig bevist?"),
            t(
                "No. The events, dates and observatories are real and "
                "documented. The numerology is a symbolic reading of the "
                "dates — an interpretive lens, not a scientific finding.",
                "Nei. Hendelsene, datoene og observatoriene er reelle og "
                "dokumenterte. Numerologien er en symbolsk lesning av "
                "datoene – en tolkende linse, ikke et vitenskapelig funn.",
            ),
        ),
        (
            t("What is the Arecibo Line project?", "Hva er Arecibo Line-prosjektet?"),
            t(
                "An ongoing exploration treating iconic transmissions and "
                "detections — the Arecibo message, the Wow! signal, "
                "repeating fast radio bursts — as points along one "
                "symbolic line, read through this site's numerology "
                "method.",
                "En pågående utforskning som behandler kjente sendinger og "
                "deteksjoner – Arecibo-meldingen, WOW!-signalet, "
                "repeterende radioutbrudd – som punkter langs én symbolsk "
                "linje, lest gjennom dette nettstedets numerologimetode.",
            ),
        ),
        (
            t("Why leave the ATLAS comet unresolved?", "Hvorfor la ATLAS-kometen stå uavklart?"),
            t(
                "Because the underlying positional claim hasn't been "
                "independently verified yet. This site would rather leave "
                "a question open than present an unverified number as "
                "fact.",
                "Fordi den underliggende posisjonspåstanden ikke er "
                "uavhengig verifisert ennå. Dette nettstedet vil heller la "
                "et spørsmål stå åpent enn å presentere et uverifisert "
                "tall som fakta.",
            ),
        ),
    ]
    return dict(chapters=chapters, labels=labels, resources=resources, faqs=faqs)
