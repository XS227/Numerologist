"""Fix article authorship and drop the ChatGPT source link.

All Article rows except the Mahsa/Bita piece defaulted to "Åse Steinsland"
(the model's default author) even though none of these were literally
written by her — they're Khabat Setaei's research/reflection pieces
(some AI-assisted, per creative-research-practice-for-numerology's
source_url). Per explicit instruction: article authorship is Khabat
Setaei unless a piece was actually supplied by Åse herself, which none
of these are. Also clears the ChatGPT source_url on the creative-research
article — the "view original source" link pointing at a chatgpt.com share
link is being removed site-wide.
"""

from django.db import migrations

AUTHOR_FIXES = {
    "creative-research-practice-for-numerology": "Åse Steinsland",
    "master-number-33": "Åse Steinsland",
    "navn-og-numerologi": "Åse Steinsland",
    "hva-avslorer-tallene-i-shahnameh": "Åse Steinsland",
    "wow-signalet-og-arecibo-linjen": "Åse Steinsland",
}


def apply_fix(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    for slug in AUTHOR_FIXES:
        Article.objects.filter(slug=slug).update(author="Khabat Setaei")
    Article.objects.filter(slug="creative-research-practice-for-numerology").update(
        source_url=None
    )


def revert_fix(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    for slug, old_author in AUTHOR_FIXES.items():
        Article.objects.filter(slug=slug).update(author=old_author)
    Article.objects.filter(slug="creative-research-practice-for-numerology").update(
        source_url="https://chatgpt.com/s/dr_68fab75a5f5c8191a9bdcc5d9d024279"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0009_add_wow_signal_article"),
    ]

    operations = [
        migrations.RunPython(apply_fix, revert_fix),
    ]
