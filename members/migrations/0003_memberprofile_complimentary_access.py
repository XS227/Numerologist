from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0002_socialloginhandoff"),
    ]

    operations = [
        migrations.AddField(
            model_name="memberprofile",
            name="complimentary_access",
            field=models.BooleanField(default=False),
        ),
    ]
