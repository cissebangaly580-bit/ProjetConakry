from django.shortcuts import get_object_or_404, redirect, render

from conakry_travel_hotel.models import Agent, Chambre, Concerner, Facture, Inclure, Reservation, Voyage
from .forms import ReservationForm
from decorators import require_agent


@require_agent
def reservation_liste(request):
    reservations = Reservation.objects.all().order_by('-date_reservation')
    return render(request, 'reservations/reservation_liste.html', {'reservations': reservations})


@require_agent
def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    concerner = Concerner.objects.filter(reservation=reservation).first()
    inclure = Inclure.objects.filter(reservation=reservation).first()
    facture = Facture.objects.filter(reservation=reservation).first()
    return render(request, 'reservations/reservation_detail.html', {
        'reservation': reservation,
        'concerner': concerner,
        'inclure': inclure,
        'facture': facture,
    })


@require_agent
def reservation_form(request, pk=None):
    reservation = get_object_or_404(Reservation, pk=pk) if pk else None
    form = ReservationForm(request.POST or None, instance=reservation)
    if request.method == 'POST' and form.is_valid():
        agent, _ = Agent.objects.get_or_create(
            user=request.user,
            defaults={
                'nom': getattr(request.user, 'last_name', '') or request.user.username,
                'prenom': getattr(request.user, 'first_name', '') or '',
                'login': request.user.username,
                'role': 'agent'
            }
        )

        reservation = form.save(agent=agent)
        total = 0
        for concerner in reservation.concerner_set.all():
            total += concerner.voyage.prix * concerner.nb_personnes
        for inclure in reservation.inclure_set.all():
            nights = max((inclure.date_sortie - inclure.date_entree).days, 1)
            total += inclure.chambre.prix_nuit * nights
        Facture.objects.update_or_create(
            reservation=reservation,
            defaults={'montant': total, 'statut_paiement': 'en_attente'},
        )
        return redirect('reservation_detail', pk=reservation.pk)
    return render(request, 'reservations/reservation_conform.html', {'form': form, 'reservation': reservation})


@require_agent
def reservation_confirm_delete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        if reservation.inclure_set.exists():
            for inclure in reservation.inclure_set.all():
                chambre = inclure.chambre
                chambre.statut = 'libre'
                chambre.save()
        if reservation.concerner_set.exists():
            for concerner in reservation.concerner_set.all():
                voyage = concerner.voyage
                voyage.places_dispo += 1
                voyage.save()
        reservation.delete()
        return redirect('reservation_liste')
    return render(request, 'reservations/reservation_confir_delete.html', {'reservation': reservation})

def reservation_liste(request):
    if not request.user.is_authenticated:
        return redirect('connexion')
    reservations = Reservation.objects.all().order_by('-date_reservation')
    return render(request, 'reservations/reservation_liste.html', {'reservations': reservations})


def reservation_detail(request, pk):
    if not request.user.is_authenticated:
        return redirect('connexion')
    reservation = get_object_or_404(Reservation, pk=pk)
    concerner = Concerner.objects.filter(reservation=reservation).first()
    inclure = Inclure.objects.filter(reservation=reservation).first()
    facture = Facture.objects.filter(reservation=reservation).first()
    return render(request, 'reservations/reservation_detail.html', {
        'reservation': reservation,
        'concerner': concerner,
        'inclure': inclure,
        'facture': facture,
    })


def reservation_form(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('connexion')
    reservation = get_object_or_404(Reservation, pk=pk) if pk else None
    form = ReservationForm(request.POST or None, instance=reservation)
    if request.method == 'POST' and form.is_valid():
        # Determine Agent corresponding to current user via OneToOne link (or create it)
        agent, _ = Agent.objects.get_or_create(
            user=request.user,
            defaults={
                'nom': getattr(request.user, 'last_name', '') or request.user.username,
                'prenom': getattr(request.user, 'first_name', '') or '',
                'login': request.user.username,
                'role': 'agent'
            }
        )

        reservation = form.save(agent=agent)
        total = 0
        for concerner in reservation.concerner_set.all():
            total += concerner.voyage.prix * concerner.nb_personnes
        for inclure in reservation.inclure_set.all():
            nights = max((inclure.date_sortie - inclure.date_entree).days, 1)
            total += inclure.chambre.prix_nuit * nights
        Facture.objects.update_or_create(
            reservation=reservation,
            defaults={'montant': total, 'statut_paiement': 'en_attente'},
        )
        return redirect('reservation_detail', pk=reservation.pk)
    return render(request, 'reservations/reservation_conform.html', {'form': form, 'reservation': reservation})


def reservation_confirm_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect('connexion')
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        if reservation.inclure_set.exists():
            for inclure in reservation.inclure_set.all():
                chambre = inclure.chambre
                chambre.statut = 'libre'
                chambre.save()
        if reservation.concerner_set.exists():
            for concerner in reservation.concerner_set.all():
                voyage = concerner.voyage
                voyage.places_dispo += 1
                voyage.save()
        reservation.delete()
        return redirect('reservation_liste')
    return render(request, 'reservations/reservation_confir_delete.html', {'reservation': reservation})
