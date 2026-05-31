import os
import sys
import django
from datetime import date, timedelta

# Setup Django
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from conakry_travel_hotel.models import Agent, Client, Voyage, Chambre, Reservation, Concerner, Inclure, Facture

User = get_user_model()

def create_users_and_agents():
    # admin user
    admin, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
    if created:
        admin.set_password('Admin123!')
        admin.save()
    Agent.objects.get_or_create(user=admin, defaults={'nom': 'Admin', 'prenom': 'Super', 'login': 'admin', 'role': 'admin'})

    # agent user
    ag, created = User.objects.get_or_create(username='agent1', defaults={'email': 'agent1@example.com'})
    if created:
        ag.set_password('Agent123!')
        ag.save()
    Agent.objects.get_or_create(user=ag, defaults={'nom': 'Agent', 'prenom': 'Un', 'login': 'agent1', 'role': 'agent'})

def create_clients():
    for i in range(1, 6):
        Client.objects.get_or_create(email=f'client{i}@example.com', defaults={'nom': f'Nom{i}', 'prenom': f'Pr{i}', 'telephone': f'6100000{i}', 'adresse': 'Conakry'})

def create_voyages():
    for i in range(1, 6):
        Voyage.objects.get_or_create(destination=f'Destination{i}', defaults={
            'description': f'Desc {i}',
            'date_depart': date.today() + timedelta(days=5*i),
            'date_retour': date.today() + timedelta(days=5*i+3),
            'prix': 100000 * i,
            'places_dispo': 10,
        })

def create_chambres():
    types = ['simple', 'double', 'suite']
    for i in range(1, 11):
        num = f'{100+i}'
        Chambre.objects.get_or_create(numero=num, defaults={'type_chambre': types[i%3], 'prix_nuit': 50000 + i*5000, 'capacite': 2, 'statut': 'libre'})

def create_sample_reservation():
    client = Client.objects.first()
    voyage = Voyage.objects.first()
    chambre = Chambre.objects.filter(statut='libre').first()
    agent = Agent.objects.filter(role='agent').first()
    if client and voyage and agent:
        reservation, created = Reservation.objects.get_or_create(client=client, agent=agent, defaults={'statut': 'en_attente', 'montant_total': 0})
        if created:
            Concerner.objects.get_or_create(reservation=reservation, voyage=voyage, defaults={'nb_personnes': 1})
            if chambre:
                Inclure.objects.get_or_create(reservation=reservation, chambre=chambre, defaults={'date_entree': date.today()+timedelta(days=1), 'date_sortie': date.today()+timedelta(days=3)})
            # compute total
            total = 0
            for c in reservation.concerner_set.all():
                total += c.voyage.prix * c.nb_personnes
            for inc in reservation.inclure_set.all():
                nights = max((inc.date_sortie - inc.date_entree).days, 1)
                total += inc.chambre.prix_nuit * nights
            Facture.objects.update_or_create(reservation=reservation, defaults={'montant': total, 'statut_paiement': 'en_attente'})

def run():
    create_users_and_agents()
    create_clients()
    create_voyages()
    create_chambres()
    create_sample_reservation()
    print('Test data generated.')

if __name__ == '__main__':
    run()
