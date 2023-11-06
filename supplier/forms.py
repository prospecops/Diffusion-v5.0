from django import forms

from .models import BulkCTM, IndividualCTM


class BulkCTMForm(forms.ModelForm):
    class Meta:
        model = BulkCTM
        fields = ['ctm_name', 'lot_number', 'quantity', 'expiration_date']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
        }

class IndividualCTMForm(forms.ModelForm):
    class Meta:
        model = IndividualCTM
        fields = ['ctm_name', 'kit_serial_number', 'quantity', 'expiration_date', 'lot_number']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
        }
