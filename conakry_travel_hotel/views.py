from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from conakry_travel_hotel.models import Chambre, Client, Facture, Reservation, Voyage
from .forms import AgentForm
from decorators import require_admin


def connexion(request):
    if request.user.is_authenticated:
        return redirect('accueil')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accueil')
        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'conakry_travel_hotel/connexion.html')


def accueil(request):
    if not request.user.is_authenticated:
        return redirect('connexion')

    context = {
        'clients_count': Client.objects.count(),
        'voyages_count': Voyage.objects.count(),
        'chambres_count': Chambre.objects.count(),
        'reservations_count': Reservation.objects.count(),
        'factures_count': Facture.objects.count(),
    }
    return render(request, 'conakry_travel_hotel/accueil.html', context)


@require_admin
def agent_list(request):
    from conakry_travel_hotel.models import Agent
    agents = Agent.objects.all().order_by('nom', 'prenom')
    return render(request, 'conakry_travel_hotel/agent_list.html', {'agents': agents})


@require_admin
def agent_form(request, pk=None):
    from conakry_travel_hotel.models import Agent
    agent = Agent.objects.filter(pk=pk).first() if pk else None
    form = AgentForm(request.POST or None, instance=agent)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('agent_list')
    return render(request, 'conakry_travel_hotel/agent_form.html', {'form': form, 'agent': agent})


@require_admin
def agent_delete(request, pk):
    from conakry_travel_hotel.models import Agent
    agent = Agent.objects.filter(pk=pk).first()
    if not agent:
        return redirect('agent_list')
    if request.method == 'POST':
        agent.delete()
        return redirect('agent_list')
    return render(request, 'conakry_travel_hotel/agent_confirm_delete.html', {'agent': agent})


@require_admin
def report_ca(request):
        from django.db.models import Sum
        # Optional date filtering
        start = request.GET.get('start')
        end = request.GET.get('end')
        qs = Facture.objects.all()
        if start:
            qs = qs.filter(date_emission__date__gte=start)
        if end:
            qs = qs.filter(date_emission__date__lte=end)
        total = qs.aggregate(total=Sum('montant'))['total'] or 0
        paid = qs.filter(statut_paiement='payee').aggregate(total=Sum('montant'))['total'] or 0
        pending = qs.filter(statut_paiement='en_attente').aggregate(total=Sum('montant'))['total'] or 0
        # CSV export
        if request.GET.get('format') == 'csv':
            import csv
            from django.http import HttpResponse
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="report_ca.csv"'
            writer = csv.writer(response)
            writer.writerow(['Total', 'Paid', 'Pending', 'Start', 'End'])
            writer.writerow([total, paid, pending, start or '', end or ''])
            return response
        return render(request, 'conakry_travel_hotel/report_ca.html', {'total': total, 'paid': paid, 'pending': pending, 'start': start, 'end': end})


@require_admin
def report_occupation(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    # For occupation, we consider current status or filter via reservations dates (simple implementation)
    total_rooms = Chambre.objects.count()
    occupied_qs = Chambre.objects.filter(statut='occupee')
    occupied = occupied_qs.count()
    occupation_rate = (occupied / total_rooms * 100) if total_rooms > 0 else 0
    # CSV export
    if request.GET.get('format') == 'csv':
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report_occupation.csv"'
        writer = csv.writer(response)
        writer.writerow(['Total rooms', 'Occupied', 'Occupation %', 'Start', 'End'])
        writer.writerow([total_rooms, occupied, round(occupation_rate,2), start or '', end or ''])
        return response
    return render(request, 'conakry_travel_hotel/report_occupation.html', {'total_rooms': total_rooms, 'occupied': occupied, 'occupation_rate': round(occupation_rate,2), 'start': start, 'end': end})


def deconnexion(request):
    logout(request)
    messages.success(request, 'Vous êtes déconnecté.')
    return redirect('connexion')
