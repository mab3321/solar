# Generated by Django 4.2.3 on 2024-06-07 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("crud", "0010_invoice_file"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="invoice",
            name="file",
        ),
    ]
