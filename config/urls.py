"""
URL configuration for Gestion_Agence_hotel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from conakry_travel_hotel import views

urlpatterns = [
    path('', views.connexion, name='root'),
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
    # Gestion du personnel (agents)
    path('personnel/agents/', views.agent_list, name='agent_list'),
    path('personnel/agents/nouveau/', views.agent_form, name='agent_nouveau'),
    path('personnel/agents/<int:pk>/modifier/', views.agent_form, name='agent_modifier'),
    path('personnel/agents/<int:pk>/supprimer/', views.agent_delete, name='agent_delete'),
    path('rapports/ca/', views.report_ca, name='report_ca'),
    path('rapports/occupation/', views.report_occupation, name='report_occupation'),
]
