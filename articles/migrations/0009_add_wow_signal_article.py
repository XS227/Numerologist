"""Add "Hva tallene sier om WOW-signalet" — a numerology research-note
article drawing on the Arecibo Line project (Arecibo-Line/ in this repo).

Every date/vibration figure here was independently recomputed and verified
before writing (using the same per-part day/month/year reduction method as
the rest of the site, matching intake/forms.py's corrected engine) — the
source research note (Arecibo-Line/Numerisk_og_astronomisk_sammenheng.md)
had several arithmetic errors: it gave 1977 -> 5 (actually 6), 2012 -> 6
(actually 5), and claimed 9797 days between the Arecibo message and the
Wow! signal (the actual gap is 1003 days). None of those wrong numbers
are used here. The ATLAS comet's claimed positional overlap with the
Wow! signal region is explicitly left out — the source note itself calls
it "foreløpig" (preliminary) and it isn't something this session could
independently verify, so it isn't presented as fact.
"""

from django.db import migrations


ARTICLE_SLUG = "wow-signalet-og-arecibo-linjen"

CONTENT = """
<p>
  16. november 1974 sendte Arecibo-observatoriet en radiomelding mot
  kulehopen M13 – et binært bilde av mennesker, DNA og tall, ment å
  vare lenger enn noen av oss. Under tre år senere, 15. august 1977,
  fanget et annet teleskop opp 72 sekunder med et signal ingen siden
  har kunnet forklare. Astronomen som oppdaget det skrev bare ett ord
  i margen: «Wow!». Dette er et forsøk på å lese de to hendelsene slik
  en numerolog leser et fødselskart – ikke for å bevise noe, men for å
  lytte etter hva tallene selv sier.
</p>

<h2>Arecibo-meldingen og dens tall</h2>
<p>
  Meldingen ble sendt 16. november 1974 – dag 16, måned 11, år 1974.
  Reduserer vi hver del for seg: dagen 16 blir 1 + 6 = <strong>7</strong>,
  måneden 11 blir 1 + 1 = <strong>2</strong>, og året 1974 blir
  1 + 9 + 7 + 4 = 21 → <strong>3</strong>. Lagt sammen: 7 + 2 + 3 = 12 →
  <strong>3</strong>. Treeren er kommunikasjonens og uttrykkets tall –
  vanskelig å tenke seg et mer passende grunnstall for menneskehetens
  første bevisste forsøk på å si «vi er her» til noen andre.
</p>

<h2>WOW!-signalet svarer</h2>
<p>
  15. august 1977 fanget Big Ear-radioteleskopet ved Ohio State
  University opp et smalbånds signal så sterkt at det etterlot et
  tydelig avtrykk i dataene. Astronomen Jerry Ehman sirklet verdiene og
  skrev «Wow!» i margen – navnet har hengt ved siden. Dato for date:
  dagen 15 blir 1 + 5 = <strong>6</strong>, måneden 8 er allerede
  <strong>8</strong>, og året 1977 blir 1 + 9 + 7 + 7 = 24 →
  <strong>6</strong>. Lagt sammen: 6 + 8 + 6 = 20 → <strong>2</strong>.
  Der Arecibo-meldingen bar treerens utadvendte «vi er her», bærer
  WOW!-signalet toerens stillere energi – mottak, balanse, et ekko som
  lytter tilbake i stedet for å rope.
</p>

<h2>1003 dager mellom sending og svar</h2>
<p>
  Fra 16. november 1974 til 15. august 1977 gikk det nøyaktig 1003
  dager. Kvertsifret: 1 + 0 + 0 + 3 = <strong>4</strong> – byggerens
  tall, stabilitet og struktur. Det er fristende å lese noe stort inn i
  et slikt tidsrom, men det ærligste vi kan si er dette: mellom et
  budskap sendt i treerens ånd og et signal mottatt i toerens, ligger
  det en fireners avstand – en periode som, numerologisk sett, handler
  om å bygge grunnen før neste steg kan tas.
</p>

<h2>FRB 121102 – ekkoet som gjentar seg</h2>
<p>
  2. november 2012 oppdaget nettopp Arecibo-observatoriet en
  radiokilde langt utenfor Melkeveien, senere kalt FRB 121102. Den ble
  det første fast radioutbruddet som noen gang er bekreftet å gjenta
  seg – samme kilde, om og om igjen, i motsetning til de fleste FRB-er
  som blinker én gang og forsvinner. At det var det samme
  observatoriet som sendte meldingen i 1974 som fanget opp dette
  gjentakende ekkoet 38 år senere, er i seg selv verdt å legge merke
  til – uavhengig av numerologien. Datoen 2. november 2012 reduseres
  slik: dagen 2 er <strong>2</strong>, måneden 11 blir
  <strong>2</strong>, og året 2012 blir 2 + 0 + 1 + 2 = <strong>5</strong>.
  Lagt sammen: 2 + 2 + 5 = <strong>9</strong> – fullendelsens og
  gjentakelsens tall, passende for en kilde hvis egenskap nettopp er å
  gjenta seg. Selve katalogbetegnelsen «121102» bærer også sitt eget
  tall: 1 + 2 + 1 + 1 + 0 + 2 = 7 – søkerens og innsiktens tall.
</p>

<h2>Hva med ATLAS-kometen?</h2>
<p>
  Arecibo Line-prosjektets forskningsnotat stiller også spørsmålet om
  kometen C/2019 Y4 (ATLAS), oppdaget i desember 2019, kan ha passert
  gjennom samme himmelfelt som WOW!-signalet kom fra. Det er et
  interessant spørsmål, men notatet selv kaller beregningene
  «foreløpige», og det finnes ikke grunnlag i dette prosjektet ennå
  til å si noe sikkert om en slik overlapping. Vi lar spørsmålet stå
  åpent, som en av tingene Arecibo Line-prosjektet fortsatt
  undersøker, i stedet for å oppgi koordinater vi ikke kan stå inne
  for.
</p>

<h2>Tall, ikke bevis</h2>
<p>
  Ingenting her beviser at Arecibo-meldingen og WOW!-signalet henger
  sammen i noen fysisk forstand – de er adskilt av lysår og
  tilfeldigheter vi ikke kan kontrollere for. Det numerologien kan
  gjøre, er å tilby et språk for undringen selv: at en melding sendt i
  treerens ånd, et signal mottatt i toerens, og en fireners avstand
  mellom dem, danner et mønster som er verdt å sitte med – ikke fordi
  det er vitenskapelig bevist, men fordi mennesker i uminnelige tider
  har lett etter mening i tallene som omgir de store øyeblikkene.
  Arecibo Line-prosjektet fortsetter å samle inn og undersøke flere
  slike hendelser; dette notatet er ett skritt på veien, ikke et
  endelig svar.
</p>
""".strip()


def add_article(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Article.objects.update_or_create(
        slug=ARTICLE_SLUG,
        defaults={
            "title": "Hva tallene sier om WOW-signalet",
            "content": CONTENT,
            "author": "Åse Steinsland",
        },
    )


def remove_article(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Article.objects.filter(slug=ARTICLE_SLUG).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0008_translate_creative_research_to_norwegian"),
    ]

    operations = [
        migrations.RunPython(add_article, remove_article),
    ]
