from django import forms

from conakry_travel_hotel.models import Chambre, Client, Concerner, Inclure, Reservation, Voyage


class ReservationForm(forms.ModelForm):
    voyage = forms.ModelChoiceField(
        queryset=Voyage.objects.filter(places_dispo__gt=0),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    chambre = forms.ModelChoiceField(
        queryset=Chambre.objects.filter(statut='libre'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    check_in = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    check_out = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    nb_personnes = forms.IntegerField(
        min_value=1,
        initial=1,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reservation
        fields = ['client', 'statut']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        voyage = cleaned_data.get('voyage')
        chambre = cleaned_data.get('chambre')
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if not voyage and not chambre:
            raise forms.ValidationError('Vous devez choisir au moins un voyage ou une chambre.')

        if chambre and (not check_in or not check_out):
            raise forms.ValidationError('Les dates d’entrée et de sortie sont requises pour une réservation de chambre.')

        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError('La date de sortie doit être après la date d’entrée.')

        return cleaned_data

    def save(self, commit=True, agent=None):
        # Allow passing an Agent instance (or None). If agent provided, ensure it's set on the reservation.
        if agent is not None:
            reservation = super().save(commit=False)
            reservation.agent = agent
            if commit:
                reservation.save()
        else:
            reservation = super().save(commit=commit)

        voyage = self.cleaned_data.get('voyage')
        chambre = self.cleaned_data.get('chambre')
        check_in = self.cleaned_data.get('check_in')
        check_out = self.cleaned_data.get('check_out')
        nb_personnes = self.cleaned_data.get('nb_personnes') or 1

        # Related objects require reservation.pk; ensure reservation is saved
        if not reservation.pk:
            if commit:
                reservation.save()
            else:
                # Can't create related objects when reservation is not saved
                return reservation

        if voyage:
            Concerner.objects.get_or_create(reservation=reservation, voyage=voyage, defaults={'nb_personnes': nb_personnes})
            if voyage.places_dispo > 0:
                voyage.places_dispo -= 1
                voyage.save()

        if chambre:
            Inclure.objects.get_or_create(
                reservation=reservation,
                chambre=chambre,
                defaults={
                    'date_entree': check_in,
                    'date_sortie': check_out,
                }
            )
            chambre.statut = 'occupee'
            chambre.save()

        return reservation
