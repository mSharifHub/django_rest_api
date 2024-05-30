# Generated by Django 4.2.13 on 2024-05-27 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0004_alter_watchlist_platform"),
    ]

    operations = [
        migrations.AlterField(
            model_name="watchlist",
            name="platform",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="watchlist",
                to="api.streamingplatform",
            ),
        ),
    ]
