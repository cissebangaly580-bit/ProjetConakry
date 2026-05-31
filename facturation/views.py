from django.shortcuts import get_object_or_404, redirect, render

from conakry_travel_hotel.models import Facture, Inclure, Reservation
from .forms import PaiementForm
from decorators import require_comptable


@require_comptable
def facture_liste(request):
    factures = Facture.objects.all().order_by('-date_emission')
    return render(request, 'facturation/facture_liste.html', {'factures': factures})


@require_comptable
def facture_detail(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    reservation = facture.reservation
    inclures = Inclure.objects.filter(reservation=reservation)
    return render(request, 'facturation/facture_detail.html', {
        'facture': facture,
        'reservation': reservation,
        'inclures': inclures,
    })


@require_comptable
def paiement(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    form = PaiementForm(request.POST or None, instance=facture)
    if request.method == 'POST' and form.is_valid():
        facture = form.save(commit=False)
        facture.statut_paiement = 'payee'
        facture.save()
        return redirect('facture_detail', pk=facture.pk)
    return render(request, 'facturation/paiment.html', {'facture': facture, 'form': form})


@require_comptable
def recu(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    return render(request, 'facturation/recu.html', {'facture': facture})
