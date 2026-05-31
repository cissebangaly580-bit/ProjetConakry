import os
import sys
import django
from datetime import date

# Ensure project root is on sys.path
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from conakry_travel_hotel.models import Chambre
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

# Create chambre
numero = 'C-101'
data = {
    'numero': numero,
    'type_chambre': 'double',
    'prix_nuit': '50000.00',
    'capacite': '2',
    'statut': 'libre',
}
resp = client.post('/hotel/nouveau/', data, follow=True)
print('Create status code:', resp.status_code)

# Check list
resp = client.get('/hotel/')
print('List status code:', resp.status_code)
if numero in resp.content.decode('utf-8'):
    print('Created chambre visible in list')
else:
    print('Created chambre NOT visible in list')

# Find created chambre
chambre = Chambre.objects.filter(numero=numero).first()
print('Chambre created id:', getattr(chambre, 'pk', None))
if chambre:
    # Detail
    resp = client.get(f'/hotel/{chambre.pk}/')
    print('Detail status:', resp.status_code)
    # Update
    upd = data.copy()
    upd['prix_nuit'] = '60000.00'
    resp = client.post(f'/hotel/{chambre.pk}/modifier/', upd, follow=True)
    print('Update status:', resp.status_code)
    chambre.refresh_from_db()
    print('Updated prix_nuit:', chambre.prix_nuit)
    # Checkin
    resp = client.post(f'/hotel/{chambre.pk}/checkin/', {}, follow=True)
    print('Checkin status:', resp.status_code)
    chambre.refresh_from_db()
    print('Statut after checkin:', chambre.statut)
    # Checkout
    resp = client.post(f'/hotel/{chambre.pk}/checkout/', {}, follow=True)
    print('Checkout status:', resp.status_code)
    chambre.refresh_from_db()
    print('Statut after checkout:', chambre.statut)
    # Delete
    resp = client.post(f'/hotel/{chambre.pk}/supprimer/', {}, follow=True)
    print('Delete status:', resp.status_code)
    exists = Chambre.objects.filter(pk=chambre.pk).exists()
    print('Chambre exists after delete:', exists)
else:
    print('No chambre found to test detail/update/delete')
