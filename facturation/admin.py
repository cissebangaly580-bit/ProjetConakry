from django.contrib import admin
from .models import Facture

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):

    # ✅ Colonnes affichées dans la liste
    list_display = [
        'id',
        'get_client',
        'montant',
        'mode_paiement',
        'statut_paiement',
        'date_emission',
    ]

    # ✅ Filtres sur la droite
    list_filter = [
        'statut_paiement',
        'mode_paiement',
        'date_emission',
    ]

    # ✅ Barre de recherche
    search_fields = [
        'reservation__client__nom',
        'reservation__client__prenom',
        'reservation__client__email',
    ]

    # ✅ Champs non modifiables (générés automatiquement)
    readonly_fields = [
        'date_emission',
        'montant',
    ]

    # ✅ Ordre d'affichage (plus récent en premier)
    ordering = ['-date_emission']

    # ✅ Méthode pour afficher le nom du client
    def get_client(self, obj):
        return obj.reservation.client
    get_client.short_description = 'Client'