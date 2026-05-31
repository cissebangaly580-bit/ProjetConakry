from django import forms

from conakry_travel_hotel.models import Facture


class PaiementForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['mode_paiement']
        widgets = {
            'mode_paiement': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('mode_paiement')
        if not payment_method:
            raise forms.ValidationError('Veuillez choisir un mode de paiement.')
        return cleaned_data
