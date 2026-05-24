from django.contrib import admin
from django.urls import path, include
from conakry_travel_hotel import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('connexion/', views.connexion, name='connexion'),
    path('accueil/', views.accueil, name='accueil'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),

    # Apps des membres
    path('clients/', include('gestion_clients.urls')),
    path('voyages/', include('gestion_voyages.urls')),
    path('hotel/', include('gestion_hotel.urls')),
    path('reservations/', include('reservations.urls')),
    path('factures/', include('facturation.urls')),
]