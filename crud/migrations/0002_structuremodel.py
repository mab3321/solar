# Generated by Django 4.2.3 on 2024-05-06 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crud", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StructureModel",
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
                ("length", models.CharField(max_length=100)),
                ("width", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
