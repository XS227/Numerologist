"""Two Norwegian articles on numbers in the Quran and in the life of the
Prophet Muhammad.

The first replaces the static /quranian-numerology/ project page (which now
redirects here). Its Surah calculator used a flat sum and dropped master
numbers; the article version follows Åse's method (each part reduced on its
own, 11/22/33 kept). Unverifiable claims from the old page were replaced by
figures that can be checked: 114 surahs, 6236 verses (Kufan count), the
abjad values of إيمان (102) and كفر (300).

The second is new. Every figure was computed with the site's own reduction
(intake.forms.IntakeForm) before writing: محمد = 92 → 11, MUHAMMAD = 29 → 11,
surah 47 → 11, the uncertain birth date 20/22 April 570 → 9 / 11. The text
is written as a respectful symbolic reflection, not a religious claim.
"""

from django.db import migrations


QURAN_SLUG = "tallene-i-koranen"
PROPHET_SLUG = "profeten-muhammads-tall"

QURAN_CONTENT = """
<p>
  Koranen er delt inn med en presisjon som inviterer til å telle: 114 suraer,
  6236 vers, en åpningssure på sju vers. Dette prosjektet leser tallene sure
  for sure – ikke for å bevise noe om teksten, men for å se hvilke mønstre som
  trer fram når vi regner slik Åse regner.
</p>

<h2>Koranen som tallstruktur</h2>
<p>
  Koranen har 114 suraer. Legger vi sammen sifrene, får vi 1 + 1 + 4 = 6.
  Etter den vanligste (kufiske) tellingen har den 6236 vers:
  6 + 2 + 3 + 6 = 17, og 1 + 7 = 8.
</p>
<p>
  Den første suraen, Al-Fatiha – «Åpningen» – har 7 vers. Dermed står tre tall
  side om side i selve rammen rundt teksten: 6 i antall suraer, 7 i åpningen og
  8 i antall vers.
</p>

<h2>Slik regner vi</h2>
<p>
  Vi bruker samme metode som resten av nettstedet. Hver del reduseres for seg
  før delene legges sammen, og mestertallene 11, 22 og 33 beholdes når de
  oppstår.
</p>
<p>
  For en sure betyr det at surenummeret og antall vers reduseres hver for seg
  og deretter legges sammen. En samlet sum kan gi et mestertall som egentlig
  ikke finnes – eller skjule et som gjør det.
</p>
<p>
  Arabiske ord regnes med abjad, der hver bokstav har en fast verdi
  (alif = 1, mim = 40, ra = 200 …). Summen reduseres på samme måte.
</p>

<h2>6, 7 og 8 – en pulsmodell</h2>
<p>
  Hovedhypotesen i prosjektet er at 6, 7 og 8 danner en svingning, som en puls:
</p>
<ul>
  <li><strong>6 – lav:</strong> det magnetiske fundamentet.</li>
  <li><strong>7 – midt:</strong> terskelen, punktet der fasen låses.</li>
  <li><strong>8 – høy:</strong> den elektriske utladningen.</li>
</ul>
<p>
  I denne modellen er 7 et overgangspunkt som skyver bevisstheten mellom det
  jordiske (6) og det kosmiske (8). At rammen rundt Koranen gir nettopp 6, 7 og
  8, er utgangspunktet for resten av undersøkelsen.
</p>

<h2>Regn på en sure</h2>
<p>
  Velg en sure. Kalkulatoren reduserer surenummeret og antall vers hver for
  seg, legger dem sammen og viser hvor resultatet står i 6–7–8-modellen.
</p>

<h2>Tro og vantro gir samme tall</h2>
<p>
  إيمان (iman, tro) har abjad-verdien 1 + 10 + 40 + 1 + 50 = 102, som gir 3.
  كفر (kufr, vantro) har verdien 20 + 80 + 200 = 300, som også gir 3.
</p>
<p>
  To motsatte ord får samme tall. Prosjektet leser dette som en mulig
  interferens-symmetri: tro og vantro kan utløse beslektede reaksjoner i
  tallsystemet, uavhengig av den moralske rammen rundt dem.
</p>

<h2>Åpningen og renheten</h2>
<p>
  Al-Fatiha er sure 1 med 7 vers: 1 + 7 = 8. Al-Ikhlas – «Renheten», den korte
  suraen om Guds enhet – er sure 112 med 4 vers. 112 gir 4, og 4 + 4 = 8.
</p>
<p>
  Den første suraen og suraen om enheten ender dermed begge i 8, den høye
  polen i modellen.
</p>

<h2>Åpne spørsmål</h2>
<p>
  Prosjektet undersøker også grammatiske mønstre, kalt P1–P6, som en mulig
  binær kode. Hvis disse sekvensene fortsetter å danne stabile bølger, kan
  teksten fungere som et koherenssignal for dem som leser og lytter.
</p>
<p>
  Dette er et utforskende forskningsprosjekt i numerologi. Funnene er
  hypoteser til studium og samtale – ikke teologiske påstander, og ikke et
  forsøk på å forklare en hellig tekst.
</p>
"""

PROPHET_CONTENT = """
<p>
  Få navn er uttalt oftere i verden enn Muhammad. Denne artikkelen leser
  tallene rundt profeten Muhammad – fred være med ham – med samme metode som
  resten av nettstedet: navnet, datoen og årene i livet hans.
</p>

<h2>Med respekt</h2>
<p>
  Numerologi er ikke en del av islamsk tro, og mange muslimer ser med skepsis
  på den. Denne teksten er en symbolsk refleksjon, skrevet med respekt. Den
  påstår ikke noe om profetens rolle eller om troen.
</p>
<p>
  Av samme grunn viser vi ingen bilder av ham – bare tallene.
</p>

<h2>Navnet i abjad</h2>
<p>
  På arabisk skrives navnet محمد, med fire bokstaver: mim, ha, mim og dal.
  I abjad har de verdiene 40, 8, 40 og 4.
</p>
<p>
  Summen er 92. Reduksjonen gir 9 + 2 = <strong>11</strong> – et mestertall.
  I numerologien er 11 inspirasjonens tall: budbæreren som tar imot og gir
  videre.
</p>

<h2>Navnet med Åses metode</h2>
<p>
  Skrevet med latinske bokstaver og regnet med Åses bokstavtabell gir
  MUHAMMAD 4 + 3 + 8 + 1 + 4 + 4 + 1 + 4 = 29, og 2 + 9 = <strong>11</strong>.
</p>
<p>
  To helt ulike alfabeter, to ulike tabeller – og samme mestertall.
</p>
<p>
  Vokalene U, A og A gir sjelstallet 5: bevegelse og frihet. Konsonantene M, H,
  M, M og D gir personlighetstallet 6: omsorg og ansvar for fellesskapet.
</p>

<h2>Sura 47 og navnet i Koranen</h2>
<p>
  Navnet Muhammad står fire ganger i Koranen (3:144, 33:40, 47:2 og 48:29).
  Navneformen Ahmad står én gang (61:6).
</p>
<p>
  Sura 47 bærer navnet hans. 4 + 7 = <strong>11</strong> – det samme
  mestertallet som navnet gir, både i abjad og med latinske bokstaver.
</p>

<h2>Fødselsdatoen vi ikke kjenner sikkert</h2>
<p>
  Tradisjonen plasserer fødselen i Elefantens år, den 12. i måneden Rabi
  al-Awwal. Omregnet til vår kalender oppgis ofte rundt 20.–22. april 570 –
  men den nøyaktige datoen er usikker.
</p>
<p>
  Derfor viser vi begge de vanligste datoene. 20. april 570 gir livsveistallet
  9: fullføring. 22. april 570 gir 22 + 4 + 3 = 29 → <strong>11</strong>:
  igjen mestertallet.
</p>
<p>
  Vi velger ikke mellom dem. Usikkerheten er en del av bildet.
</p>

<h2>Tallene i livet hans</h2>
<p>
  Den første åpenbaringen kom da han var 40 år – tallet 4, grunnmuren.
  Åpenbaringen varte i 23 år, som gir 5: forandring. Utvandringen til Medina,
  hijra, skjedde i 622, som gir 1: en ny begynnelse, og starten på den
  islamske tidsregningen.
</p>
<p>
  Han døde 63 år gammel etter månekalenderen. 6 + 3 = 9: fullføringens tall.
</p>

<h2>Hva tallene kan fortelle</h2>
<p>
  Det mest påfallende er gjentakelsen av 11: i navnet på arabisk, i navnet på
  latin og i suraen som bærer navnet. I numerologien er 11 tallet for den som
  tar imot inspirasjon og gir den videre.
</p>
<p>
  Ved siden av står 9 – fullføringen – i den ene fødselsdatoen og i alderen
  ved bortgangen. I Koranen (33:40) kalles han «profetenes segl».
</p>
<p>
  Tallene beviser ingenting. Men de kan være en inngang til å reflektere over
  et liv som har formet milliarder av mennesker.
</p>
"""


def add_articles(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Article.objects.update_or_create(
        slug=QURAN_SLUG,
        defaults={
            "title": "Tallene i Koranen: 6, 7 og 8",
            "content": QURAN_CONTENT,
            "author": "Khabat Setaei",
        },
    )
    Article.objects.update_or_create(
        slug=PROPHET_SLUG,
        defaults={
            "title": "Profeten Muhammads tall: navnet, datoen og mestertallet 11",
            "content": PROPHET_CONTENT,
            "author": "Khabat Setaei",
        },
    )


def remove_articles(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Article.objects.filter(slug__in=[QURAN_SLUG, PROPHET_SLUG]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0010_fix_article_authors"),
    ]

    operations = [
        migrations.RunPython(add_articles, remove_articles),
    ]
