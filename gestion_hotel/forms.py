from django import forms

from conakry_travel_hotel.models import Chambre


class ChambreForm(forms.ModelForm):
    class Meta:
        model = Chambre
        fields = ['numero', 'type_chambre', 'capacite', 'prix_nuit', 'statut']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'type_chambre': forms.Select(attrs={'class': 'form-control'}),
            'capacite': forms.NumberInput(attrs={'class': 'form-control'}),
            'prix_nuit': forms.NumberInput(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }
