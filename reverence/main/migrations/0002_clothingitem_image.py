# Generated by Django 5.1.6 on 2025-02-26 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="clothingitem",
            name="image",
            field=models.ImageField(blank=True, upload_to="product/%Y/%m/%d"),
        ),
    ]
