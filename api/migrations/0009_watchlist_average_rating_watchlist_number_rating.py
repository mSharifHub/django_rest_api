# Generated by Django 4.2.13 on 2024-05-30 10:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0008_review_reviewer"),
    ]

    operations = [
        migrations.AddField(
            model_name="watchlist",
            name="average_rating",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="watchlist",
            name="number_rating",
            field=models.IntegerField(default=0),
        ),
    ]
