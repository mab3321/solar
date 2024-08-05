from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *
from django.forms import modelformset_factory
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class SolarPanelForm(forms.ModelForm):
    class Meta:
        model = SolarPanel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class InverterForm(forms.ModelForm):
    class Meta:
        model = Inverter
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class StructureForm(forms.ModelForm):
    class Meta:
        model = Structure
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class CablingForm(forms.ModelForm):
    class Meta:
        model = Cabling
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class NetMeteringForm(forms.ModelForm):
    class Meta:
        model = NetMetering
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
class BatteriesForm(forms.ModelForm):
    class Meta:
        model = Batteries
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
class LightningArrestorForm(forms.ModelForm):
    class Meta:
        model = LightningArrestor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
class InstallationForm(forms.ModelForm):
    class Meta:
        model = Installation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        # Get all instances for each related model
        client_choices = [(client.pk, str(client.name)) for client in Client.objects.all()]
        solar_panel_choices = [(solar_panel.pk, str(solar_panel.name)) for solar_panel in SolarPanel.objects.all()]
        inverter_choices = [(inverter.pk, str(inverter.name)) for inverter in Inverter.objects.all()]
        structure_choices = [(structure.pk, str(structure.name)) for structure in Structure.objects.all()]
        cabling_choices = [(cabling.pk, str(cabling.name)) for cabling in Cabling.objects.all()]
        net_metering_choices = [(net_metering.pk, str(net_metering.name)) for net_metering in NetMetering.objects.all()]
                # Update choices for each ForeignKey field
        self.fields['name'].choices = client_choices
        self.fields['solar_panel'].choices = solar_panel_choices
        self.fields['inverter'].choices = inverter_choices
        self.fields['structure'].choices = structure_choices
        self.fields['cabling'].choices = cabling_choices
        self.fields['net_metering'].choices = net_metering_choices
        

ClientFormSet = modelformset_factory(Client, form=ClientForm, extra=1)
InvoiceFormSet = modelformset_factory(Invoice, form=InvoiceForm, extra=0)