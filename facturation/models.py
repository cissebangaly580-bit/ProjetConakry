from django.db import models

# Create your models here.
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
    montant = models.DecimalField(max_digits=10, decimal_places=2)