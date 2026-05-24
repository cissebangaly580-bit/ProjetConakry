from django.urls import path
from . import views

urlpatterns = [
    path('generer/<int:reservation_id>/', views.generer_facture, name='generer_facture'),
    path('<int:facture_id>/', views.detail_facture, name='detail_facture'),
    path('historique/', views.historique_paiements, name='historique_paiements'),
    path('en-attente/', views.factures_en_attente, name='factures_en_attente'),
]