from django.urls import path
from . import views

urlpatterns = [
    path('', views.chambre_liste, name='chambre_liste'),
    path('nouveau/', views.chambre_form, name='chambre_nouveau'),
    path('<int:pk>/', views.chambre_detail, name='chambre_detail'),
    path('<int:pk>/modifier/', views.chambre_form, name='chambre_modifier'),
    path('<int:pk>/supprimer/', views.chambre_confirm_delete, name='chambre_supprimer'),
    path('<int:pk>/checkin/', views.checkin, name='chambre_checkin'),
    path('<int:pk>/checkout/', views.checkout, name='chambre_checkout'),
]