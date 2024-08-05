# Generated by Django 4.2.3 on 2024-06-07 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crud", "0012_invoice_cabling_price_invoice_cabling_quantity_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="discount",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                help_text="Enter discount as a percentage.",
                max_digits=15,
            ),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="solar_panel_price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
