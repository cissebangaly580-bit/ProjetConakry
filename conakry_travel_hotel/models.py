from django.db import models


class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    adresse = models.TextField(blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Voyage(models.Model):
    destination = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_depart = models.DateField()
    date_retour = models.DateField()
    prix = models.DecimalField(max_digits=15, decimal_places=2)
    places_dispo = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.destination} ({self.date_depart})"


class Chambre(models.Model):
    TYPES_CHAMBRE = [
        ('simple', 'Simple'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    ]
    STATUTS_CHAMBRE = [
        ('libre', 'Libre'),
        ('occupee', 'Occupée'),
        ('maintenance', 'En maintenance'),
    ]

    numero = models.CharField(max_length=10, unique=True)
    type_chambre = models.CharField(max_length=20, choices=TYPES_CHAMBRE, default='simple')
    prix_nuit = models.DecimalField(max_digits=15, decimal_places=2)
    capacite = models.PositiveIntegerField(default=1)
    statut = models.CharField(max_length=20, choices=STATUTS_CHAMBRE, default='libre')

    def __str__(self):
        return f"Chambre {self.numero}"


class Agent(models.Model):
    ROLES = [
        ('agent', 'Agent de voyage'),
        ('receptionniste', 'Réceptionniste'),
        ('comptable', 'Comptable'),
        ('admin', 'Administrateur'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    login = models.CharField(max_length=50, unique=True)
    mdp_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLES, default='agent')

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Reservation(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée'),
    ]

    date_reservation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    montant_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    def __str__(self):
        return f"Réservation #{self.id} - {self.client}"


class Concerner(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    nb_personnes = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('reservation', 'voyage')

    def __str__(self):
        return f"{self.voyage} x{self.nb_personnes}"


class Inclure(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    date_entree = models.DateField()
    date_sortie = models.DateField()

    def __str__(self):
        return f"Chambre {self.chambre.numero} du {self.date_entree} au {self.date_sortie}"


class Facture(models.Model):
    STATUTS_PAIEMENT = [
        ('payee', 'Payée'),
        ('en_attente', 'En attente'),
        ('annulee', 'Annulée'),
    ]
    MODES_PAIEMENT = [
        ('especes', 'Espèces'),
        ('orange_money', 'Orange Money'),
        ('mtn_momo', 'MTN MoMo'),
    ]

    date_emission = models.DateTimeField(auto_now_add=True)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    statut_paiement = models.CharField(max_length=20, choices=STATUTS_PAIEMENT, default='en_attente')
    mode_paiement = models.CharField(max_length=20, choices=MODES_PAIEMENT, blank=True, null=True)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)

    def __str__(self):
        return f"Facture #{self.id} - {self.montant} GNF"