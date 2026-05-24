# conakry_travel_hotel/models.py
class Facture(models.Model):
    PAIEMENTS = [
        ('especes', 'Espèces'),
        ('orange_money', 'Orange Money'),
        ('mtn_momo', 'MTN MoMo'),
    ]
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    date_emission = models.DateField(auto_now_add=True)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    statut_paiement = models.CharField(max_length=20, default='en_attente')
    mode_paiement = models.CharField(max_length=20, choices=PAIEMENTS, blank=True)

    def __str__(self):
        return f'Facture {self.id}'