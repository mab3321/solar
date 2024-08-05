import django_filters
from .models import *

class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        fields = '__all__'

class SolarPanelFilter(django_filters.FilterSet):
    class Meta:
        model = SolarPanel
        fields = '__all__'

class InverterFilter(django_filters.FilterSet):
    class Meta:
        model = Inverter
        fields = '__all__'

class StructureFilter(django_filters.FilterSet):
    class Meta:
        model = Structure
        fields = '__all__'

class CablingFilter(django_filters.FilterSet):
    class Meta:
        model = Cabling
        fields = '__all__'

class NetMeteringFilter(django_filters.FilterSet):
    class Meta:
        model = NetMetering
        fields = '__all__'

class BatteriesFilter(django_filters.FilterSet):
    class Meta:
        model = Batteries
        fields = '__all__'

class LightningArrestorFilter(django_filters.FilterSet):
    class Meta:
        model = LightningArrestor
        fields = '__all__'

class InstallationFilter(django_filters.FilterSet):
    class Meta:
        model = Installation
        fields = '__all__'

class InvoiceFilter(django_filters.FilterSet):
    class Meta:
        model = Invoice
        fields = '__all__'
class ExpendituresFilter(django_filters.FilterSet):
    class Meta:
        model = Expenditures
        fields = '__all__'