# Generated by Django 4.2.7 on 2023-11-21 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_account", "0006_page"),
    ]

    operations = [
        migrations.AddField(
            model_name="tvshow",
            name="views",
            field=models.IntegerField(default=0),
        ),
    ]
