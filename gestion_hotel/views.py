from django.shortcuts import get_object_or_404, redirect, render

from conakry_travel_hotel.models import Chambre
from .forms import ChambreForm
from decorators import require_agent, require_receptionniste


def chambre_liste(request):
    if not request.user.is_authenticated:
        return redirect('connexion')
    chambres = Chambre.objects.all().order_by('numero')
    return render(request, 'gestion_hotel/chambre.liste.html', {'chambres': chambres})


def chambre_detail(request, pk):
    if not request.user.is_authenticated:
        return redirect('connexion')
    chambre = get_object_or_404(Chambre, pk=pk)
    return render(request, 'gestion_hotel/chambre.detail.html', {'chambre': chambre})


@require_agent
def chambre_form(request, pk=None):
    chambre = get_object_or_404(Chambre, pk=pk) if pk else None
    form = ChambreForm(request.POST or None, instance=chambre)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('chambre_liste')
    return render(request, 'gestion_hotel/chambre.form.html', {'form': form, 'chambre': chambre})


@require_agent
def chambre_confirm_delete(request, pk):
    chambre = get_object_or_404(Chambre, pk=pk)
    if request.method == 'POST':
        chambre.delete()
        return redirect('chambre_liste')
    return render(request, 'gestion_hotel/chambre_confirm_detete.html', {'chambre': chambre})


@require_receptionniste
def checkin(request, pk):
    chambre = get_object_or_404(Chambre, pk=pk)
    if request.method == 'POST':
        chambre.statut = 'occupee'
        chambre.save()
        return redirect('chambre_detail', pk=pk)
    return render(request, 'gestion_hotel/checkin.html', {'chambre': chambre})


@require_receptionniste
def checkout(request, pk):
    chambre = get_object_or_404(Chambre, pk=pk)
    if request.method == 'POST':
        chambre.statut = 'libre'
        chambre.save()
        return redirect('chambre_detail', pk=pk)
    return render(request, 'gestion_hotel/checkout.html', {'chambre': chambre})
