from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from conakry_travel_hotel.models import Facture, Reservation

# ✅ RG4 : Toute réservation confirmée génère une facture
@login_required
def generer_facture(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # Vérifier que la réservation est confirmée (RG4)
    if reservation.statut != 'confirmee':
        messages.error(request, "❌ Seules les réservations confirmées peuvent générer une facture.")
        return redirect('liste_reservations')

    # Calcul automatique du montant
    montant = 0
    if reservation.chambre:
        montant += reservation.chambre.prix_nuit
    if reservation.voyage:
        montant += reservation.voyage.prix

    # Mettre à jour montant total de la réservation
    reservation.montant_total = montant
    reservation.save()

    # Créer la facture si elle n'existe pas encore
    facture, created = Facture.objects.get_or_create(
        reservation=reservation,
        defaults={'montant': montant}
    )

    if created:
        messages.success(request, "✅ Facture générée avec succès !")
    else:
        messages.info(request, "ℹ️ La facture existe déjà.")

    return redirect('detail_facture', facture_id=facture.id)


# ✅ Détail facture + paiement (RG6 et RG7)
@login_required
def detail_facture(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)

    if request.method == 'POST':
        mode = request.POST.get('mode_paiement')
        montant_recu = request.POST.get('montant_recu')

        # RG6 : Facture payée si montant reçu >= montant dû
        if float(montant_recu) >= float(facture.montant):
            facture.mode_paiement = mode
            facture.statut_paiement = 'paye'
            facture.save()
            messages.success(request, "✅ Paiement enregistré avec succès !")
            return redirect('historique_paiements')
        else:
            messages.error(request, "❌ Le montant reçu est insuffisant.")

    return render(request, 'facturation/facture_detail.html', {'facture': facture})


# ✅ Historique avec filtre par statut
@login_required
def historique_paiements(request):
    statut = request.GET.get('statut', '')
    if statut:
        factures = Facture.objects.filter(
            statut_paiement=statut
        ).order_by('-date_emission')
    else:
        factures = Facture.objects.all().order_by('-date_emission')

    return render(request, 'facturation/historique.html', {
        'factures': factures,
        'statut_filtre': statut
    })


# ✅ Liste des factures en attente
@login_required
def factures_en_attente(request):
    factures = Facture.objects.filter(
        statut_paiement='en_attente'
    ).order_by('date_emission')

    return render(request, 'facturation/en_attente.html', {'factures': factures})