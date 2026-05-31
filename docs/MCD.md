# Modèle Conceptuel de Données (MCD) — Conakry Travel & Hôtel

Entités principales :

- Client (nom, prenom, email, telephone, adresse)
- Agent (user*, nom, prenom, login, role)
- Voyage (destination, description, date_depart, date_retour, prix, places_dispo)
- Chambre (numero, type_chambre, prix_nuit, capacite, statut)
- Reservation (date_reservation, statut, montant_total, client_id, agent_id)
- Concerner (reservation_id, voyage_id, nb_personnes)
- Inclure (reservation_id, chambre_id, date_entree, date_sortie)
- Facture (date_emission, montant, statut_paiement, mode_paiement, reservation_id)

Relations principales :
- Un `Client` peut avoir plusieurs `Reservation`.
- Une `Reservation` est liée à un `Agent` (responsable) et à un `Client`.
- Une `Reservation` peut concerner plusieurs `Voyage` via `Concerner`.
- Une `Reservation` peut inclure une ou plusieurs `Chambre` via `Inclure`.
- Une `Reservation` a une `Facture` (OneToOne).

(* : l'attribut `user` lie l'entité Agent au compte Django `User` dans la mise en œuvre.)
