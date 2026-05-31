from django.shortcuts import get_object_or_404, redirect, render

from conakry_travel_hotel.models import Voyage
from .forms import VoyageForm
from decorators import require_agent


def voyage_liste(request):
    if not request.user.is_authenticated:
        return redirect('connexion')
    voyages = Voyage.objects.all().order_by('date_depart')
    return render(request, 'gestion_voyages/voyage_liste.html', {'voyages': voyages})


def voyage_detail(request, pk):
    if not request.user.is_authenticated:
        return redirect('connexion')
    voyage = get_object_or_404(Voyage, pk=pk)
    return render(request, 'gestion_voyages/voyage_detail.html', {'voyage': voyage})


@require_agent
def voyage_form(request, pk=None):
    voyage = get_object_or_404(Voyage, pk=pk) if pk else None
    form = VoyageForm(request.POST or None, instance=voyage)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('voyage_liste')
    return render(request, 'gestion_voyages/voyage_form.html', {'form': form, 'voyage': voyage})


@require_agent
def voyage_confirme_delete(request, pk):
    voyage = get_object_or_404(Voyage, pk=pk)
    if request.method == 'POST':
        voyage.delete()
        return redirect('voyage_liste')
    return render(request, 'gestion_voyages/voyage_confirme_delete.html', {'voyage': voyage})
