# Dans conakry_travel_hotel/models.py
class Facture(models.Model):
    MODES_PAIEMENT = [
        ('especes', 'Espèces'),
        ('orange_money', 'Orange Money'),
        ('mtn_momo', 'MTN MoMo'),
    ]
    STATUTS = [
        ('en_attente', 'En attente'),
        ('paye', 'Payée'),
    ]
    reservation = models.OneToOneField(
        Reservation, on_delete=models.CASCADE, related_name='facture'
    )
    date_emission = models.DateField(auto_now_add=True)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    statut_paiement = models.CharField(
        max_length=20, choices=STATUTS, default='en_attente'
    )
    mode_paiement = models.CharField(
        max_length=20, choices=MODES_PAIEMENT, blank=True
    )

    def __str__(self):
        return f'Facture N°{self.id} — {self.reservation.client}'