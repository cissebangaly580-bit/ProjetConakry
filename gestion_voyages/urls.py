from django.urls import path
from . import views

urlpatterns = [
    path('', views.voyage_liste, name='voyage_liste'),
    path('nouveau/', views.voyage_form, name='voyage_nouveau'),
    path('<int:pk>/', views.voyage_detail, name='voyage_detail'),
    path('<int:pk>/modifier/', views.voyage_form, name='voyage_modifier'),
    path('<int:pk>/supprimer/', views.voyage_confirme_delete, name='voyage_supprimer'),
]