from django.shortcuts import render

# Create your views here.
def connexion(request):
    return render(request, 'connexion.html')
def accueil(request):
    return render(request, 'accueil.html')
def deconnexion(request):
    return render(request, 'deconnexion.html')
