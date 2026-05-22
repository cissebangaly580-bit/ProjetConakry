
from django.db import models
class Facture(models.Model):
MODE_PAIEMENT = [
('Especes', 'Espèces'),
('MobileMoney', 'Mobile Money'),
]
STATUT_FACTURE = [
('Paye', 'Payé'),
('NonPaye', 'Non payé'),
]
numero_facture = models.CharField(max_length=20, unique=True)
client = models.CharField(max_length=100)
montant = models.DecimalField(max_digits=12, decimal_places=2)
statut = models.CharField(
max_length=20,
choices=STATUT_FACTURE,
default='NonPaye'
)
paiement = models.CharField(
max_length=20,
choices=MODE_PAIEMENT
)
date_creation = models.DateTimeField(auto_now_add=True)
def __str__(self):
return self.numero_facture