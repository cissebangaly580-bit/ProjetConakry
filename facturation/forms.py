from django import forms
from .models import Facture


class FactureForm(forms.ModelForm):

    class Meta:
        model = Facture

        fields = [
            'numero_facture',
            'client',
            'montant',
            'mode_paiement',
            'statut'
        ]