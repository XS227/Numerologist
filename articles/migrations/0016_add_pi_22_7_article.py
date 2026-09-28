from django.db import migrations

SLUG = "22-7-riktig-beregning-av-pi"

CONTENT = """
<p><strong>22/7 er en av matematikkens mest kjente π-brøker – og i Åses numerologiske rammeverk får akkurat 22 og 7 et ekstra symbolsk lag.</strong> Denne artikkelen undersøker regnestykket, den repeterende sekvensen 142857, sirkelgeometrien, historikken og den numerologiske tolkningen.</p>

<h2>22 delt på 7</h2>
<p>22/7 = 3,142857142857… Den repeterende sekvensen 142857 er en direkte konsekvens av syvendedeler og danner et fascinerende syklisk mønster.</p>

<h2>Matematisk presisjon</h2>
<p>π = 3,141592653589… og er ikke identisk med 22/7. Forskjellen er omtrent 0,0012644893, eller cirka 0,04025 prosent relativt. 22/7 er derfor en svært kjent og enkel tilnærming, men ikke den eksakte verdien av π.</p>

<h2>142857 – syklusen</h2>
<p>Tallet 142857 er syklisk: når det multipliseres med 1 til 6, kommer de samme sifrene tilbake i rotert rekkefølge. Dette gjør syvendedeler spesielt visuelt og pedagogisk interessante.</p>

<h2>Sirkelen og 22/7</h2>
<p>For en sirkel med diameter 7 gir 22/7 en beregnet omkrets på nøyaktig 22. Med π blir omkretsen omtrent 21,9911486. Den lille forskjellen viser både styrken og begrensningen i brøken.</p>

<h2>22 og 7 i numerologien</h2>
<p>I numerologisk tradisjon omtales 22 som et mestertall knyttet til struktur og manifestasjon, mens 7 forbindes med analyse, søken og fordypning. Dette er et symbolsk tolkningslag og må skilles fra matematisk bevis.</p>

<h2>Hva kan bevises?</h2>
<p>Vi kan bevise regnestykket, avviket fra π og 142857-mønsteret. At 22 og 7 danner en meningsbærende numerologisk nøkkel er en tolkning i Åses metode. Den spesialbygde siden lar leseren utforske begge lag interaktivt.</p>
"""

def add_article(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Article.objects.update_or_create(
        slug=SLUG,
        defaults={
            "title": "22/7 – hvorfor 22 delt på 7 er den riktige beregningen av π",
            "content": CONTENT,
            "author": "Numerologist · Åses metode",
        },
    )

def remove_article(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Article.objects.filter(slug=SLUG).delete()

class Migration(migrations.Migration):
    dependencies = [("articles", "0015_add_ase_archive_batch2")]
    operations = [migrations.RunPython(add_article, remove_article)]
