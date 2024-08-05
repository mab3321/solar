# Generated by Django 4.2.3 on 2024-05-17 07:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("crud", "0006_remove_structure_h_beam_remove_structure_l2_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="invoice",
            name="status",
            field=models.CharField(
                choices=[
                    ("QUOTE", "Quote"),
                    ("PARTIALLY_PAID", "Partially Paid"),
                    ("UNPAID", "Unpaid"),
                ],
                default="QUOTE",
                max_length=15,
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="client",
            name="area",
            field=models.CharField(
                help_text="You Area (i.e DHA, Gulberg, etc.)", max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="client",
            name="monthly_consumption_units",
            field=models.IntegerField(
                help_text="Monthly consumption in units", null=True
            ),
        ),
    ]