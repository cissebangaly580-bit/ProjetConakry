import os
import sys
import django
from datetime import datetime

proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core import management

OUT_DIR = os.path.join(proj_root, 'fixtures')
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_file = os.path.join(OUT_DIR, f'initial_data_{now}.json')
    # Export only project apps
    apps = ['conakry_travel_hotel', 'gestion_clients', 'gestion_voyages', 'gestion_hotel', 'reservations', 'facturation']
    with open(out_file, 'w', encoding='utf-8') as f:
        management.call_command('dumpdata', *apps, stdout=f)
    print('Fixtures exported to', out_file)

if __name__ == '__main__':
    run()
