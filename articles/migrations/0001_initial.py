# Generated manually for initial Article model.
from typing import List, Tuple

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies: List[Tuple[str, str]] = []

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(unique=True)),
                ("content", models.TextField()),
                ("author", models.CharField(default="Åse Steinsland", max_length=100)),
                ("source_url", models.URLField(blank=True, null=True)),
                ("published", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-published"]},
        ),
    ]
