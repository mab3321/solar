from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone
from django.urls import reverse
from django.utils.timezone import now
from django.core.exceptions import ValidationError

from datetime import datetime
class Utility():
    @classmethod
    def get_field_labels(cls):
        # Returns a list of tuples (field name, field label)
        res = [(field.name, field.verbose_name) for field in cls._meta.fields]
        print(f"Meta Fields are {cls._meta.fields}")
        print(f"Res is {res}")
        return res

class Client(models.Model,Utility):
    cnic = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    company = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(max_length=100,help_text="You Area (i.e DHA, Gulberg, etc.)")
    contact_number = models.CharField(max_length=20)
    monthly_consumption_units = models.IntegerField(null=True,help_text="Monthly consumption in units")
class SolarPanel(models.Model,Utility):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50,null=True, blank=True)
    capacity = models.CharField(max_length=50)
    price = models.FloatField(null=True, blank=True)

class Inverter(models.Model,Utility):
    name = models.CharField(max_length=100)
    choice = models.CharField(max_length=100)
    capacity = models.CharField(max_length=50)
    price = models.FloatField(null=True, blank=True)
class Structure(models.Model,Utility):
    name = models.CharField(max_length=50,null=True, blank=True)
    brand = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True)
class Cabling(models.Model,Utility):
    name = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True)

class NetMetering(models.Model,Utility):
    name = models.CharField(max_length=100)
    phase_type = models.CharField(max_length=50)
    price = models.FloatField(null=True, blank=True)

class Batteries(models.Model,Utility):
    name = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True)

class LightningArrestor(models.Model,Utility):
    name = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True)

class Installation(models.Model,Utility):
    name = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True)

class PartiallyPaid(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PartiallyPaid: {self.client.name} - {self.amount}"
# Define the Invoice model incorporating fields from other models

class Invoice(models.Model, Utility):
    STATUS_CHOICES = [
        ('QUOTE', 'Quote'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('PAID', 'Paid'),
    ]
    
    name = models.ForeignKey('Client', on_delete=models.DO_NOTHING, null=True, blank=True)
    solar_panel = models.ForeignKey('SolarPanel', on_delete=models.DO_NOTHING, null=True, blank=True)
    solar_panel_quantity = models.IntegerField(default=0)
    solar_panel_price = models.DecimalField(max_digits=10, decimal_places=2)

    inverter = models.ForeignKey('Inverter', on_delete=models.DO_NOTHING, null=True, blank=True)
    inverter_quantity = models.IntegerField(default=0)
    inverter_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

    structure = models.ForeignKey('Structure', on_delete=models.DO_NOTHING, null=True, blank=True)
    structure_quantity = models.IntegerField(default=0)
    structure_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

    cabling = models.ForeignKey('Cabling', on_delete=models.DO_NOTHING, null=True, blank=True)
    cabling_quantity = models.IntegerField(default=0)
    cabling_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

    net_metering = models.ForeignKey('NetMetering', on_delete=models.DO_NOTHING, null=True, blank=True)
    net_metering_quantity = models.IntegerField(default=0)
    net_metering_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

    battery = models.ForeignKey('Batteries', on_delete=models.DO_NOTHING, null=True, blank=True)
    battery_quantity = models.IntegerField(default=0)
    battery_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

    lightning_arrestor = models.ForeignKey('LightningArrestor', on_delete=models.DO_NOTHING, null=True, blank=True)
    lightning_arrestor_quantity = models.IntegerField(default=0)
    lightning_arrestor_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

    installation = models.ForeignKey('Installation', on_delete=models.DO_NOTHING, null=True, blank=True)
    installation_quantity = models.IntegerField(default=0)
    installation_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

    discount = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, help_text="Enter discount.")
    shipping_charges = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, help_text="Enter shipping charges.")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='QUOTE')
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, help_text="Enter amount paid for partially paid invoices.")
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_download_url(self):
        """Return a URL for downloading the invoice."""
        return reverse('download-invoice', kwargs={'invoice_id': self.pk})

    def __str__(self):
        return f"Invoice {self.id} - {self.name.name}"

    def save(self, *args, **kwargs):
        if self.status == 'PARTIALLY_PAID':
            if self.amount_paid <= 0:
                raise ValidationError("Amount paid must be provided for partially paid invoices.")
            
            # Check if this is an update with an actual change in amount_paid
            if self.pk is not None:
                original = Invoice.objects.get(pk=self.pk)
                if original.amount_paid != self.amount_paid:
                    PartiallyPaid.objects.create(
                        client=self.name,
                        invoice=self,
                        amount=self.amount_paid
                    )
            else:
                PartiallyPaid.objects.create(
                    client=self.name,
                    invoice=self,
                    amount=self.amount_paid
                )

        super().save(*args, **kwargs)

