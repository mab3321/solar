# Generated by Django 4.2.3 on 2024-06-10 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("crud", "0016_client_company"),
    ]

    operations = [
        migrations.RenameField(
            model_name="client",
            old_name="contract_number",
            new_name="contact_number",
        ),
    ]