# Rapport final — Conakry Travel & Hôtel

Résumé des livrables fournis :

- Cahier des charges (fournit par le client) : fonctionnalités et périmètre.
- Code source complet dans le dépôt (modules : `conakry_travel_hotel`, `gestion_clients`, `gestion_voyages`, `gestion_hotel`, `reservations`, `facturation`).
- Base de données : schéma PostgreSQL. Migrations appliquées (voir `conakry_travel_hotel/migrations`).
- Fonctionnalités implémentées :
  - Gestion clients CRUD
  - Gestion voyages CRUD
  - Gestion chambres CRUD, check-in / check-out
  - Réservations combinées voyage + hébergement
  - Facturation et paiement (espèces / Mobile Money placeholders)
  - Gestion des rôles et droits d'accès (Agent / Réceptionniste / Comptable / Admin)
  - Interface d'administration simplifiée pour `Agent`
  - Rapports CA et occupation (CSV export)
  - Scripts d'automatisation : génération de données tests, export fixtures, sauvegarde

Tests automatisés: scripts `scripts/verify_*.py` fournis et exécutés avec succès localement.

Recommandations & étapes suivantes :
- Intégrer une authentification plus stricte et gestion des mots de passe d'agents via le modèle `User` uniquement.
- Compléter l'interface admin pour gestion complète des utilisateurs et assignation de rôles.
- Mettre en place un job planifié (cron / Task Scheduler) pour exécuter `scripts/backup_data.py` quotidiennement (script ajouté).
- Préparer le déploiement en production (paramètres `ALLOWED_HOSTS`, variables d'environnement, SSL, sauvegardes hors-site).

Contacts et manuel utilisateur : voir `docs/manual_utilisateur.md`.
