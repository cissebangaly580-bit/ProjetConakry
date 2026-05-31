import os
import sys
import django
from datetime import date, timedelta

# Ensure project root is on sys.path
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from conakry_travel_hotel.models import Voyage, Chambre, Client as ClientModel, Reservation, Facture
from django.conf import settings

# Create or reuse test superuser
User = get_user_model()
username = 'autotest'
password = 'Autotest123!'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email='auto@example.com', password=password)

client = Client()
# Allow test client host
try:
    settings.ALLOWED_HOSTS += ['testserver', '127.0.0.1', 'localhost']
except Exception:
    settings.ALLOWED_HOSTS = ['testserver', '127.0.0.1', 'localhost']

logged = client.login(username=username, password=password)
print('Login success:', logged)

# Create or get voyage
voyage = Voyage.objects.filter(destination='ReserveVille').first()
if not voyage:
    voyage = Voyage.objects.create(
        destination='ReserveVille',
        description='Test reserve',
        date_depart=date.today() + timedelta(days=5),
        date_retour=date.today() + timedelta(days=10),
        prix=200000.00,
        places_dispo=5,
    )
# Create or get chambre
chambre, _ = Chambre.objects.get_or_create(
    numero='R-201',
    defaults={
        'type_chambre': 'simple',
        'prix_nuit': 75000.00,
        'capacite': 1,
        'statut': 'libre',
    }
)
# Create or get client
client_model, _ = ClientModel.objects.get_or_create(email='john.doe@example.com', defaults={'nom': 'Doe', 'prenom': 'John', 'telephone': '12345678', 'adresse': 'Test'})

# Prepare reservation data (voyage only)
res_data = {
    'client': str(client_model.pk),
    'statut': 'en_attente',
    'voyage': str(voyage.pk),
    'nb_personnes': '2',
}
try:
    resp = client.post('/reservations/nouveau/', res_data, follow=True)
    print('Reservation create status:', resp.status_code)
    # Check reservation exists
    reservation = Reservation.objects.filter(client=client_model).first()
except Exception as e:
    print('POST to reservation view raised exception:', e)
    reservation = None
print('Reservation id:', getattr(reservation, 'pk', None))
if reservation:
    # Check facture created
    facture = Facture.objects.filter(reservation=reservation).first()
    print('Facture exists:', facture is not None)
    if facture:
        print('Facture montant:', facture.montant, 'statut:', facture.statut_paiement)
        # Test payment
        pay_resp = client.post(f'/factures/{facture.pk}/payer/', {'mode_paiement': 'especes'}, follow=True)
        print('Paiement status code:', pay_resp.status_code)
        facture.refresh_from_db()
        print('Facture statut après paiement:', facture.statut_paiement)
    else:
        print('Aucune facture générée')
else:
    print('Réservation non créée via POST; tentative de création manuelle via ORM')
    # Create an Agent and build reservation manually
    from conakry_travel_hotel.models import Agent, Concerner, Inclure
    # Create or get Agent linked to test user via OneToOne
    agent_obj, _ = Agent.objects.get_or_create(
        user=User.objects.get(username=username),
        defaults={'nom': 'Auto', 'prenom': 'Test', 'role': 'agent'}
    )
    reservation = Reservation.objects.create(client=client_model, agent=agent_obj, statut='en_attente', montant_total=0)
    # create concerner
    Concerner.objects.create(reservation=reservation, voyage=voyage, nb_personnes=2)
    # Optionally create inclure if chambre selected
    Inclure.objects.create(reservation=reservation, chambre=chambre, date_entree=date.today()+timedelta(days=1), date_sortie=date.today()+timedelta(days=3))
    # adjust voyage places and chambre statut
    voyage.places_dispo = max(voyage.places_dispo - 1, 0)
    voyage.save()
    chambre.statut = 'occupee'
    chambre.save()
    # compute total and create facture
    total = 0
    total += voyage.prix * 2
    nights = 2
    total += chambre.prix_nuit * nights
    Facture.objects.update_or_create(reservation=reservation, defaults={'montant': total, 'statut_paiement': 'en_attente'})
    facture = Facture.objects.filter(reservation=reservation).first()
    print('Reservation created manually id:', reservation.pk)
    print('Facture created manually:', facture is not None, getattr(facture, 'montant', None))
    # Test payment
    pay_resp = client.post(f'/factures/{facture.pk}/payer/', {'mode_paiement': 'especes'}, follow=True)
    print('Paiement status code:', pay_resp.status_code)
    facture.refresh_from_db()
    print('Facture statut après paiement:', facture.statut_paiement)
