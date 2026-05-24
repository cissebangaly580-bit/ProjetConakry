from django.contrib import admin
from .models import Facture

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['id', 'reservation', 'montant', 'statut_paiement', 'mode_paiement', 'date_emission']
    list_filter = ['statut_paiement', 'mode_paiement']