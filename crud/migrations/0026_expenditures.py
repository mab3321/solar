# Generated by Django 4.2.3 on 2024-08-05 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("crud", "0025_partiallypaid"),
    ]

    operations = [
        migrations.CreateModel(
            name="Expenditures",
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
                ("name", models.CharField(max_length=100)),
                ("value", models.FloatField()),
                (
                    "inv_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="crud.invoice",
                    ),
                ),
            ],
        ),
    ]
