from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Facture, Reservation

# ✅ Générer une facture depuis une réservation
@login_required
def generer_facture(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # 🔢 Calcul automatique du montant
    montant = 0
    if reservation.chambre:
        montant += reservation.chambre.prix_nuit
    if reservation.voyage:
        montant += reservation.voyage.prix

    # Mettre à jour le montant total de la réservation
    reservation.montant_total = montant
    reservation.save()

    # Créer la facture si elle n'existe pas encore
    facture, created = Facture.objects.get_or_create(
        reservation=reservation,
        defaults={'montant': montant}
    )
    return redirect('detail_facture', facture_id=facture.id)


# ✅ Détail d'une facture + choisir le mode de paiement
@login_required
def detail_facture(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)
    if request.method == 'POST':
        mode = request.POST.get('mode_paiement')
        facture.mode_paiement = mode
        facture.statut_paiement = 'paye'
        facture.save()
        return redirect('historique_paiements')
    return render(request, 'facturation/facture_detail.html', {'facture': facture})


# ✅ Historique avec filtre par statut
@login_required
def historique_paiements(request):
    statut = request.GET.get('statut', '')  # filtre depuis l'URL
    if statut:
        factures = Facture.objects.filter(statut_paiement=statut).order_by('-date_emission')
    else:
        factures = Facture.objects.all().order_by('-date_emission')
    return render(request, 'facturation/historique.html', {
        'factures': factures,
        'statut_filtre': statut
    })