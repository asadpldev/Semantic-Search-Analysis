# Generated by Django 4.2.7 on 2023-11-21 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_account", "0005_alter_comment_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Page",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
                ("link", models.URLField()),
                ("details", models.TextField()),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
