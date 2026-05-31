from django.urls import path
from . import views

urlpatterns = [
    path("", views.clients_liste, name="clients_liste"),
    path("nouveau/", views.client_form, name="client_create"),
    path("<int:pk>/", views.client_detail, name="client_detail"),
    path("<int:pk>/modifier/", views.client_form, name="client_update"),
    path("<int:pk>/supprimer/", views.client_confirm_delete, name="client_confirm_delete"),
]
