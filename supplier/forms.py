from django import forms
from depots.models import Depot  # Import Depot
from .models import BulkCTM, IndividualCTM


class AssignInventoryForm(forms.Form):
    depot = forms.ModelChoiceField(queryset=Depot.objects.all())
    bulk_ctms = forms.ModelMultipleChoiceField(queryset=BulkCTM.objects.filter(depot=None), required=False)
    individual_ctms = forms.ModelMultipleChoiceField(queryset=IndividualCTM.objects.filter(depot=None), required=False)


class BulkCTMForm(forms.ModelForm):
    class Meta:
        model = BulkCTM
        fields = ['device', 'lot_number', 'quantity', 'expiration_date', 'depot']  # Added 'depot' field
        widgets = {
            'expiration_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }


class IndividualCTMForm(forms.ModelForm):
    class Meta:
        model = IndividualCTM
        fields = ['device', 'kit_serial_number', 'quantity', 'expiration_date', 'lot_number',
                  'depot']  # Added 'depot' field
        widgets = {
            'expiration_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
