from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation_liste, name='reservation_liste'),
    path('nouveau/', views.reservation_form, name='reservation_nouveau'),
    path('<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('<int:pk>/modifier/', views.reservation_form, name='reservation_modifier'),
    path('<int:pk>/supprimer/', views.reservation_confirm_delete, name='reservation_supprimer'),
]