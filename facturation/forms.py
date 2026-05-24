from django import forms
from .models import Facture

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['reservation', 'montant', 'mode_paiement', 'statut_paiement']
        widgets = {
            'reservation': forms.Select(attrs={'style': 'padding:8px; width:100%;'}),
            'montant': forms.NumberInput(attrs={'style': 'padding:8px; width:100%;', 'placeholder': 'Ex: 500000'}),
            'mode_paiement': forms.Select(attrs={'style': 'padding:8px; width:100%;'}),
            'statut_paiement': forms.Select(attrs={'style': 'padding:8px; width:100%;'}),
        }