from django.shortcuts import get_object_or_404, redirect, render

from conakry_travel_hotel.models import Client
from .forms import ClientForm
from decorators import require_agent


def clients_liste(request):
    if not request.user.is_authenticated:
        return redirect('connexion')
    clients = Client.objects.all().order_by('nom', 'prenom')
    return render(request, 'gestion_clients/clients_liste.html', {'clients': clients})


def client_detail(request, pk):
    if not request.user.is_authenticated:
        return redirect('connexion')
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'gestion_clients/client_detail.html', {'client': client})


@require_agent
def client_form(request, pk=None):
    client = get_object_or_404(Client, pk=pk) if pk else None
    form = ClientForm(request.POST or None, instance=client)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('clients_liste')
    return render(request, 'gestion_clients/clients_forms.html', {'form': form, 'client': client})


@require_agent
def client_confirm_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('clients_liste')
    return render(request, 'gestion_clients/client_confirm_delete.html', {'client': client})
