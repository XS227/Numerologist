from django.db import migrations

def add_ase_archive_batch1(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    from articles.ase_archive_batch1 import AUTHOR, BATCH
    for item in BATCH:
        Article.objects.update_or_create(
            slug=item["slug"],
            defaults={
                "title": item["title"],
                "content": item["content"],
                "author": AUTHOR,
                "source_url": item["source_url"],
            },
        )

def remove_ase_archive_batch1(apps, schema_editor):
    Article = apps.get_model("articles", "Article")
    from articles.ase_archive_batch1 import BATCH
    Article.objects.filter(slug__in=[item["slug"] for item in BATCH]).delete()

class Migration(migrations.Migration):
    dependencies = [("articles", "0013_expand_elon_musk_business_family")]
    operations = [migrations.RunPython(add_ase_archive_batch1, remove_ase_archive_batch1)]

