from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from conakry_travel_hotel.models import Reservation
from .models import Facture
from .forms import FactureForm


@login_required
def generer_facture(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.statut != 'confirmee':
        messages.error(request, "Seules les réservations confirmées peuvent générer une facture.")
        return redirect('liste_factures')
    montant = 0
    if hasattr(reservation, 'chambre') and reservation.chambre:
        montant += reservation.chambre.prix_nuit
    if hasattr(reservation, 'voyage') and reservation.voyage:
        montant += reservation.voyage.prix
    reservation.montant_total = montant
    reservation.save()
    facture, created = Facture.objects.get_or_create(
        reservation=reservation,
        defaults={'montant': montant}
    )
    if created:
        messages.success(request, "Facture générée avec succès !")
    else:
        messages.info(request, "La facture existe déjà.")
    return redirect('detail_facture', facture_id=facture.id)


@login_required
def detail_facture(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    if request.method == 'POST':
        mode = request.POST.get('mode_paiement')
        montant_recu = request.POST.get('montant_recu')
        if float(montant_recu) >= float(facture.montant):
            facture.mode_paiement = mode
            facture.statut_paiement = 'payee'
            facture.save()
            messages.success(request, "Paiement enregistré avec succès !")
            return redirect('liste_factures')
        else:
            messages.error(request, "Le montant reçu est insuffisant.")
    return render(request, 'facturation/facture_detail.html', {'facture': facture})


@login_required
def historique_paiements(request):
    statut = request.GET.get('statut', '')
    if statut:
        factures = Facture.objects.filter(statut_paiement=statut).order_by('-date_emission')
    else:
        factures = Facture.objects.all().order_by('-date_emission')
    return render(request, 'facturation/historique.html', {
        'factures': factures,
        'statut_filtre': statut
    })


@login_required
def factures_en_attente(request):
    factures = Facture.objects.filter(statut_paiement='en_attente').order_by('date_emission')
    return render(request, 'facturation/en_attente.html', {'factures': factures})


@login_required
def ajouter_facture(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Facture enregistrée avec succès !")
            return redirect('liste_factures')
    else:
        form = FactureForm()
    return render(request, 'facturation/ajouter_facture.html', {'form': form})


@login_required
def liste_factures(request):
    factures = Facture.objects.all().order_by('-date_emission')
    return render(request, 'facturation/facture_liste.html', {'factures': factures})