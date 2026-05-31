from django.urls import path
from . import views

urlpatterns = [
    path('', views.facture_liste, name='facture_liste'),
    path('<int:pk>/', views.facture_detail, name='facture_detail'),
    path('<int:pk>/payer/', views.paiement, name='facture_paiement'),
    path('<int:pk>/recu/', views.recu, name='facture_recu'),
]