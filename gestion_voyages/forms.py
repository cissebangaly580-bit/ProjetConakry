from django import forms

from conakry_travel_hotel.models import Voyage


class VoyageForm(forms.ModelForm):
    class Meta:
        model = Voyage
        fields = ['destination', 'description', 'date_depart', 'date_retour', 'prix', 'places_dispo']
        widgets = {
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_depart': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_retour': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
            'places_dispo': forms.NumberInput(attrs={'class': 'form-control'}),
        }
