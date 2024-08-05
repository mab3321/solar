from rest_framework import serializers
from .models import *  # Import your models accordingly

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
class SolarPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarPanel
        fields = '__all__'
class InverterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inverter
        fields = '__all__'
class StructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = '__all__'
class CablingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabling
        fields = '__all__'

class NetMeteringSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetMetering
        fields = '__all__'
class BatteriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batteries
        fields = '__all__'
class LightningArrestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightningArrestor
        fields = '__all__'
class InstallationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installation
        fields = '__all__'
class InvoiceSerializer(serializers.ModelSerializer):
    # Use nested serializers for GET requests
    class Meta:
        model = Invoice
        fields = '__all__'