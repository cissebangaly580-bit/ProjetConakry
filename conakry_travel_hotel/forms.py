from django import forms
from django.contrib.auth import get_user_model
from conakry_travel_hotel.models import Agent

User = get_user_model()


class AgentForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Agent
        fields = ['user', 'nom', 'prenom', 'login', 'role']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'login': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
