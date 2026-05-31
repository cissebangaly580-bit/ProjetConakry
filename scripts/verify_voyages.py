import os
import sys
import django
from datetime import date, timedelta

# Ensure project root is on sys.path so Django settings module can be imported
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from conakry_travel_hotel.models import Voyage
from django.conf import settings

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

# Create voyage
data = {
    'destination': 'TestVille',
    'description': 'Desc',
    'date_depart': (date.today() + timedelta(days=10)).isoformat(),
    'date_retour': (date.today() + timedelta(days=15)).isoformat(),
    'prix': '100000.00',
    'places_dispo': '10',
}
resp = client.post('/voyages/nouveau/', data, follow=True)
print('Create status code:', resp.status_code)

# Check list
resp = client.get('/voyages/')
print('List status code:', resp.status_code)
if 'TestVille' in resp.content.decode('utf-8'):
    print('Created voyage visible in list')
else:
    print('Created voyage NOT visible in list')

# Find created voyage
voyage = Voyage.objects.filter(destination='TestVille').first()
print('Voyage created id:', getattr(voyage, 'pk', None))
if voyage:
    # Detail
    resp = client.get(f'/voyages/{voyage.pk}/')
    print('Detail status:', resp.status_code)
    # Update
    upd = data.copy()
    upd['destination'] = 'TestVilleUpdated'
    resp = client.post(f'/voyages/{voyage.pk}/modifier/', upd, follow=True)
    print('Update status:', resp.status_code)
    voyage.refresh_from_db()
    print('Updated destination:', voyage.destination)
    # Delete
    resp = client.post(f'/voyages/{voyage.pk}/supprimer/', {}, follow=True)
    print('Delete status:', resp.status_code)
    exists = Voyage.objects.filter(pk=voyage.pk).exists()
    print('Voyage exists after delete:', exists)
else:
    print('No voyage found to test detail/update/delete')
