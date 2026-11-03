from django.db import migrations

SLUG = "louis-vuitton-lv-55"

CONTENT = """
<p><strong>To bokstaver. Ett monogram. Et romertall: LV = 55.</strong> Denne NAMNum-studien følger merkevaren fra Louis Vuittons fødsel i 1821, via grunnleggelsen i 1854 og monogrammet i 1896, til 130-årsmarkeringen i 2026. Vi utforsker mønstre, men skiller tallfakta fra symbolsk tolkning.</p>

<h2>LV = 55 · symbolet</h2>
<p>Romertallet L = 50 og V = 5, derfor LV = 55. Numerologisk redusert blir dette 5 + 5 = 10 → 1. Monogrammet ble imidlertid designet av Georges Vuitton i 1896 med farens initialer, ikke som en dokumentert referanse til tallet 55. Dette er et treff mellom et kjent monogram og romertallssystemet, ikke bevis på skjult markedsføring.</p>

<h2>Louis Vuitton · to alfabet, ett resultat</h2>
<p>Pytagoreisk gir LOUIS = 22 og VUITTON = 31, altså 53 → 8. Kaldeisk gir LOUIS = 20 og VUITTON = 33, også 53 → 8. I den pytagoreiske beregningen gir begge navnedelenes vokaler 18 → 9. Identisk totalsum i to systemer er verdt å undersøke, men kan oppstå uten design eller hensikt.</p>

<h2>Familien · tallene går i arv</h2>
<p>Louis Vuitton ble født 4. august 1821. Sifrene i hele datoen gir 24 → 6; fødselsdagen er 4. Navnet til sønnen Georges Vuitton gir pytagoreisk 40 + 31 = 71 → 8, mens Louis Vuitton gir 53 → 8. Begge fornavn reduseres dessuten til 4. Dette delvis felles mønsteret påvirkes naturligvis av etternavnet de deler.</p>

<h2>Årstall og avstander</h2>
<p>1854, etableringsåret, gir 18 → 9. Monogramåret 1896 gir 24 → 6, samme tverrsum som grunnleggerens fullstendige fødselsdato. Fra åpningen i London i 1885 til monogrammet i 1896 er det 11 år; fra Louis Vuittons død i 1892 til monogrammet er det fire. I 2026 fyller monogrammet 130 år; 1 + 3 + 0 = 4.</p>

<h2>Menneskene bak den moderne merkevaren</h2>
<p>Bernard Arnaults navn gir 59 → 5 etter den pytagoreiske metoden. Pietro Beccari, som har ledet Louis Vuitton siden februar 2023 og LVMH Fashion Group siden januar 2026, gir 70 → 7. Disse verdiene avhenger av skrivemåten og valgt alfabet; de sier ikke noe dokumentert om personen eller lederegenskaper.</p>

<h2>Hypotesen: Er 55 en syklus?</h2>
<p>Et strengt søk etter 55-årssykluser gir foreløpig ikke sterke treff: 1854 + 55 = 1909, 1896 + 55 = 1951 og 1987 + 55 = 2042. Ingen av de to første er tydelige hovedmilepæler i merkevarens offisielle historie. Vi bør derfor teste samme metode på mange luksusmerker før vi omtaler 55 som mer enn en interessant symbolsk forbindelse.</p>

<h2>Konklusjon og kilder</h2>
<p>De tydeligste observerte verdiene er <strong>LV = 55</strong>, <strong>Louis Vuitton = 53/8 i to alfabet</strong> og <strong>24/6 for både fødselsdato og monogramår</strong>. Tallene kan kontrolleres; betydningen er en kulturell og numerologisk fortolkning, ikke vitenskapelig forklaring på forretningssuksess.</p>
<p>Kilder: <a href="https://us.louisvuitton.com/eng-us/magazine/articles/heritage">Louis Vuitton – Heritage</a>, <a href="https://www.lvmh.com/en/news-lvmh/louis-vuitton-celebrates-130-years-of-its-monogram-a-universal-symbol-of-creativity">LVMH – 130 years of the Monogram (19.01.2026)</a>, <a href="https://www.lvmh.com/en/our-group/governance/pietro-beccari">LVMH – Pietro Beccari</a>.</p>
"""

def add_article(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Article.objects.update_or_create(
        slug=SLUG,
        defaults={
            "title": "Louis Vuitton: De skjulte tallene bak LV = 55",
            "content": CONTENT,
            "author": "NAMNum Research · SETAEI",
        },
    )

def remove_article(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Article.objects.filter(slug=SLUG).delete()

class Migration(migrations.Migration):
    dependencies = [("articles", "0016_add_pi_22_7_article")]
    operations = [migrations.RunPython(add_article, remove_article)]
