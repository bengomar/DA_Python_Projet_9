# Generated by Django 4.2.4 on 2023-08-27 15:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_alter_ticket_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="", verbose_name="image"
            ),
        ),
    ]