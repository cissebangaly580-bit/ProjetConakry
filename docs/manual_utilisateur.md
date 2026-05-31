% Manual utilisateur — Conakry Travel & Hôtel

## Connexion
- Accédez à `/connexion/` et entrez votre identifiant et mot de passe.
- Les rôles disponibles : `admin`, `agent`, `receptionniste`, `comptable`.

## Modules principaux

### Clients
- Consulter la liste des clients : `/clients/`
- Créer/modifier un client (agents) : `/clients/nouveau/` ou `/clients/<pk>/modifier/`

### Voyages
- Lister et consulter voyages : `/voyages/`
- Créer/modifier/supprimer (agents) : `/voyages/nouveau/`, `/voyages/<pk>/modifier/`

### Hôtel
- Lister chambres : `/hotel/`
- Gérer chambre (agents) : création/modification/suppression
- Check-in / check-out (réceptionniste) : `/hotel/<pk>/checkin/` et `/hotel/<pk>/checkout/`

### Réservations
- Créer une réservation combinée voyage + chambre (agents) : `/reservations/nouveau/`
- Consulter détail et facture associée : `/reservations/<pk>/`

### Facturation
- Liste des factures (comptables) : `/factures/`
- Paiement et reçu : `/factures/<pk>/payer/` et `/factures/<pk>/recu/`

### Administration du personnel
- Liste/gestion agents (admins) : `/personnel/agents/`

## Rapports
- Chiffre d'affaires : `/rapports/ca/` (filtre par date et export CSV)
- Taux d'occupation : `/rapports/occupation/` (export CSV)

## Sauvegarde
- Sauvegarde manuelle : exécuter `python scripts/backup_data.py` (génère `backups/backup_all_<timestamp>.json`)
- Import fixtures : `python manage.py loaddata fixtures/initial_data_YYYYMMDD_HHMMSS.json`
