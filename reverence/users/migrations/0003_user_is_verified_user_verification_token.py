# Generated by Django 5.1.6 on 2025-03-02 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_rename_apartament_number_user_apartment_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_verified",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="verification_token",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
