# Generated by Django 4.2.3 on 2024-05-17 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crud", "0009_rename_brand_cabling_name_rename_brand_inverter_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="invoices/"),
        ),
    ]
