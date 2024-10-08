# Generated by Django 4.2.3 on 2024-06-07 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crud", "0013_invoice_discount_alter_invoice_solar_panel_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="discount",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                help_text="Enter discount.",
                max_digits=15,
            ),
        ),
    ]
