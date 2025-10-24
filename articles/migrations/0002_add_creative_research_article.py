from django.db import migrations

ARTICLE_SLUG = "creative-research-practice-for-numerology"


CONTENT = """
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


def add_article(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Article.objects.update_or_create(
        slug=ARTICLE_SLUG,
        defaults={
            "title": "Building a Creative Research Practice for Numerology",
            "content": CONTENT,
            "source_url": "https://chatgpt.com/s/dr_68fab75a5f5c8191a9bdcc5d9d024279",
        },
    )


def remove_article(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    Article.objects.filter(slug=ARTICLE_SLUG).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_article, remove_article),
    ]
