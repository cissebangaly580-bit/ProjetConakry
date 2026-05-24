from django.db import models
from conakry_travel_hotel.models import Reservation


class Facture(models.Model):
    STATUTS_PAIEMENT = [
        ('en_attente', 'En attente'),
        ('payee', 'Payée'),
        ('annulee', 'Annulée'),
    ]
    MODES_PAIEMENT = [
        ('especes', 'Espèces'),
        ('orange_money', 'Orange Money'),
        ('mtn_momo', 'MTN MoMo'),
    ]
    date_emission = models.DateTimeField(auto_now_add=True)
    montant = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    statut_paiement = models.CharField(
        max_length=20, choices=STATUTS_PAIEMENT, default='en_attente'
    )
    mode_paiement = models.CharField(
        max_length=20, choices=MODES_PAIEMENT, blank=True, null=True
    )
    reservation = models.OneToOneField(
        Reservation, on_delete=models.CASCADE,
        related_name='facture_obj', null=True, blank=True
    )

    def __str__(self):
        return f"Facture #{self.id} - {self.montant} GNF"