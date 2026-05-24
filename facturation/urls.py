from django.urls import path
from . import views

urlpatterns = [
    # ... URLs existantes ...

    # Facturation
    path('facture/generer/<int:reservation_id>/', views.generer_facture, name='generer_facture'),
    path('facture/<int:facture_id>/', views.detail_facture, name='detail_facture'),
    path('facture/historique/', views.historique_paiements, name='historique_paiements'),
    path('facture/en-attente/', views.factures_en_attente, name='factures_en_attente'),
]