# Generated by Django 4.2.13 on 2024-05-28 07:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0006_reviews"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Reviews",
            new_name="Review",
        ),
    ]