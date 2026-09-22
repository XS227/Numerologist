"""Translate "Building a Creative Research Practice for Numerology" into
Norwegian and give it section headings.

This article was the only one of the five still English-only with no <h2>
structure at all — it rendered as one unbroken block of plain text, with
no Norwegian version for nb-language visitors (unlike the other four
articles, which are each single-language but match the site's dominant
Norwegian). Faithfully translates the existing English content (no new
claims added) and adds headings around the structure the English text
already implies (three named stages -> three named sections), so it can
get the same chapter/TOC treatment as the other articles.
"""

from django.db import migrations


ARTICLE_SLUG = "creative-research-practice-for-numerology"

OLD_TITLE = "Building a Creative Research Practice for Numerology"
OLD_CONTENT = """
<p>
  Creative work inside Numerologist Studio is often rooted in intimate
  conversations—the private questions seekers bring when they feel the numbers
  tugging at their sleeves. The new research note expands one of those
  dialogues, tracing how a quiet observation from a mentoring session grows
  into a full editorial feature that others can learn from.
</p>
<p>
  The piece follows Åse's reflections after guiding a client who feared that
  formal study would dampen their intuition. Instead of prescribing more
  exercises, Åse invited the client to map the moments when the numbers felt
  alive. That map revealed a rhythm: when the client worked in short, focused
  bursts and then paused to integrate sensations, insight arrived without
  force. The article names this cadence a <em>creative research practice</em>,
  offering a structure any reader can adapt.
</p>
<p>
  Readers are encouraged to work through three stages. First, the
  <strong>listening sweep</strong>: a 20-minute free-write that captures
  lingering questions about their Life Path or current pinnacle. Second, the
  <strong>pattern sketch</strong>: translating those notes into a visual spread
  that pairs numbers with sensory anchors—colours, textures, or sounds that
  surface during meditation. Finally, the <strong>sharing pause</strong>:
  sending a short voice note or message to a trusted partner describing what
  shifted. Each step ends with a breath practice that keeps the nervous system
  grounded while the intellect roams.
</p>
<p>
  Beyond the exercise itself, the article reflects on why naming these rituals
  matters. Numerology often gets trapped in static definitions, yet Åse argues
  that research happens each time seekers document how numbers move through
  their daily lives. By treating experimentation as scholarship, the community
  builds an archive of lived numerology—one that future students can inherit
  and expand.
</p>
<p>
  The closing section includes a gentle reminder that progress is not measured
  by how quickly a conclusion is reached. Instead, growth appears when seekers
  feel safe enough to ask bolder questions. The editorial invites readers to
  revisit their own study habits, noting where a creative research practice can
  replace rigid checklists with attentive curiosity.
</p>
""".strip()

NEW_TITLE = "Å bygge en kreativ forskningspraksis i numerologi"
NEW_CONTENT = """
<p>
  Kreativt arbeid i Numerologist Studio er ofte forankret i fortrolige
  samtaler — de private spørsmålene søkere bringer med seg når de kjenner at
  tallene drar i ermet deres. Det nye forskningsnotatet utvider en av disse
  samtalene, og følger hvordan en stille observasjon fra en veiledningstime
  vokser til en full redaksjonell artikkel som andre kan lære av.
</p>

<h2>Bakgrunnen for notatet</h2>
<p>
  Teksten følger Åses refleksjoner etter å ha veiledet en klient som fryktet
  at formell studering ville dempe intuisjonen. I stedet for å foreskrive
  flere øvelser, inviterte Åse klienten til å kartlegge øyeblikkene der
  tallene føltes levende. Kartet avslørte en rytme: når klienten jobbet i
  korte, fokuserte perioder og deretter stoppet opp for å ta innover seg
  følelsene, kom innsikten uten anstrengelse. Artikkelen kaller denne rytmen
  en <em>kreativ forskningspraksis</em>, og tilbyr en struktur enhver leser
  kan tilpasse.
</p>

<h2>Tre steg i praksisen</h2>
<p>
  Leserne oppfordres til å arbeide seg gjennom tre trinn. Først
  <strong>lytterunden</strong>: en 20-minutters fri skriveøkt som fanger opp
  spørsmål som henger igjen om livsveien eller nåværende toppunkt. Deretter
  <strong>mønsterskissen</strong>: å oversette notatene til et visuelt
  oppsett som parer tall med sanselige holdepunkter — farger, teksturer
  eller lyder som dukker opp under meditasjon. Til slutt
  <strong>delingspausen</strong>: å sende en kort talemelding eller melding
  til en betrodd partner som beskriver hva som skiftet. Hvert trinn
  avsluttes med en pusteøvelse som holder nervesystemet jordet mens
  intellektet vandrer.
</p>

<h2>Hvorfor navngivning betyr noe</h2>
<p>
  Utover selve øvelsen reflekterer artikkelen over hvorfor det betyr noe å
  navngi disse ritualene. Numerologi blir ofte fanget i statiske
  definisjoner, men Åse hevder at forskning skjer hver gang søkere
  dokumenterer hvordan tallene beveger seg gjennom hverdagen deres. Ved å
  behandle eksperimentering som forskning, bygger fellesskapet et arkiv av
  levd numerologi — ett som fremtidige studenter kan arve og bygge videre
  på.
</p>

<h2>Fremgang måles annerledes</h2>
<p>
  Den avsluttende delen inneholder en mild påminnelse om at fremgang ikke
  måles i hvor raskt man når en konklusjon. Vekst viser seg i stedet når
  søkere føler seg trygge nok til å stille dristigere spørsmål. Redaksjonelt
  inviterer artikkelen leserne til å se på nytt på egne studievaner, og
  legge merke til hvor en kreativ forskningspraksis kan erstatte rigide
  sjekklister med oppmerksom nysgjerrighet.
</p>
""".strip()


def apply_translation(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Article.objects.filter(slug=ARTICLE_SLUG).update(title=NEW_TITLE, content=NEW_CONTENT)


def revert_translation(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Article.objects.filter(slug=ARTICLE_SLUG).update(title=OLD_TITLE, content=OLD_CONTENT)


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0007_fix_bita_soul_urge_personality"),
    ]

    operations = [
        migrations.RunPython(apply_translation, revert_translation),
    ]
