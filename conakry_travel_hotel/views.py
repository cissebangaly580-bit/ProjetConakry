from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

# Create your views here.
def connexion(request):
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
    return render(request, 'conakry_travel_hotel/accueil.html')


def deconnexion(request):
    logout(request)
    messages.success(request, 'Vous êtes déconnecté.')
    return redirect('connexion')
