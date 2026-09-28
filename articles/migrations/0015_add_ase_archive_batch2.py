from django.db import migrations

OLD_NOTICE = """<p class="ase-update-note"><strong>Oppdatert utgave.</strong> Denne teksten bygger på Åse Karin Steinslands originalartikkel på Nummerologens Verden og er redigert for Numerologist. Numerologi presenteres som en symbolsk og spirituell tolkningsmetode; når artikkelen berører historie, vitenskap eller helse, skiller vi mellom dokumenterbare fakta og numerologisk tolkning.</p>"""

def add_batch2_and_clean_notice(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    from articles.ase_archive_batch2 import AUTHOR, BATCH
    for article in Article.objects.filter(author="Åse Karin Steinsland"):
        if OLD_NOTICE in article.content:
            article.content = article.content.replace(OLD_NOTICE, "", 1).lstrip()
            article.save(update_fields=["content"])
    for item in BATCH:
        Article.objects.update_or_create(
            slug=item["slug"],
            defaults={
                "title": item["title"],
                "content": item["content"].strip(),
                "author": AUTHOR,
                "source_url": item["source_url"],
            },
        )

def remove_batch2(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    from articles.ase_archive_batch2 import BATCH
    Article.objects.filter(slug__in=[item["slug"] for item in BATCH]).delete()

class Migration(migrations.Migration):
    dependencies = [("articles", "0014_add_ase_archive_batch1")]
    operations = [migrations.RunPython(add_batch2_and_clean_notice, remove_batch2)]
