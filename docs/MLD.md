# Modèle Logique des Données (MLD) — tables et colonnes principales

- conakry_travel_hotel_client
  - id (PK), nom, prenom, email (unique), telephone, adresse

- conakry_travel_hotel_agent
  - id (PK), user_id (FK -> auth_user, nullable), nom, prenom, login (unique), mdp_hash, role

- conakry_travel_hotel_voyage
  - id (PK), destination, description, date_depart, date_retour, prix (decimal), places_dispo (int)

- conakry_travel_hotel_chambre
  - id (PK), numero (unique), type_chambre, prix_nuit, capacite, statut

- conakry_travel_hotel_reservation
  - id (PK), date_reservation, statut, montant_total, client_id (FK), agent_id (FK)

- conakry_travel_hotel_concerner
  - id (PK), reservation_id (FK), voyage_id (FK), nb_personnes
  - unique(reservation_id, voyage_id)

- conakry_travel_hotel_inclure
  - id (PK), reservation_id (FK), chambre_id (FK), date_entree, date_sortie

- conakry_travel_hotel_facture
  - id (PK), date_emission, montant, statut_paiement, mode_paiement, reservation_id (OneToOne FK)
