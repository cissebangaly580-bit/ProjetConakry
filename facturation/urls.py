from django.urls import path
from . import views

urlpatterns = [
    # ... les URLs existantes ...
    path('facture/generer/<int:reservation_id>/', views.generer_facture, name='generer_facture'),
    path('facture/<int:facture_id>/', views.detail_facture, name='detail_facture'),
    path('facture/historique/', views.historique_paiements, name='historique_paiements'),
]