from database.db import get_connection, get_cursor
from datetime import date

T_RES = "conakry_travel_hotel_reservation"
T_INC = "conakry_travel_hotel_inclure"
T_CON = "conakry_travel_hotel_concerner"

def lister_reservations(statut=None):
    conn = get_connection()
    cur  = get_cursor(conn)
    q = f"""
        SELECT r.id, r.date_reservation, r.statut, r.montant_total,
               c.nom||' '||c.prenom AS client,
               a.nom||' '||a.prenom AS agent
        FROM {T_RES} r
        JOIN conakry_travel_hotel_client c ON r.client_id = c.id
        JOIN conakry_travel_hotel_agent  a ON r.agent_id  = a.id
    """
    if statut:
        cur.execute(q + " WHERE r.statut=%s ORDER BY r.date_reservation DESC", (statut,))
    else:
        cur.execute(q + " ORDER BY r.date_reservation DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def creer_reservation(client_id, agent_id, statut="en cours"):
    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        cur.execute(
            f"INSERT INTO {T_RES} (date_reservation, statut, montant_total, agent_id, client_id) VALUES (NOW(),%s,0,%s,%s) RETURNING id",
            (statut, agent_id, client_id)
        )
        res_id = cur.fetchone()["id"]
        conn.commit()
        return True, "Réservation créée.", res_id
    except Exception as e:
        conn.rollback()
        return False, f"Erreur : {e}", None
    finally:
        conn.close()

def ajouter_chambre_reservation(reservation_id, chambre_id, date_entree, date_sortie):
    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        # Vérifier disponibilité
        cur.execute(f"""
            SELECT id FROM {T_INC}
            WHERE chambre_id=%s
            AND NOT (date_sortie <= %s OR date_entree >= %s)
        """, (chambre_id, date_entree, date_sortie))
        if cur.fetchone():
            conn.close()
            return False, "Chambre non disponible pour ces dates."
        cur.execute(
            f"INSERT INTO {T_INC} (date_entree, date_sortie, chambre_id, reservation_id) VALUES (%s,%s,%s,%s)",
            (date_entree, date_sortie, chambre_id, reservation_id)
        )
        # Mettre à jour statut chambre
        cur.execute("UPDATE conakry_travel_hotel_chambre SET statut='occupée' WHERE id=%s", (chambre_id,))
        # Recalculer montant total
        _recalculer_montant(cur, reservation_id)
        conn.commit()
        return True, "Chambre ajoutée à la réservation."
    except Exception as e:
        conn.rollback()
        return False, f"Erreur : {e}"
    finally:
        conn.close()

def ajouter_voyage_reservation(reservation_id, voyage_id, nb_personnes):
    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        cur.execute(
            f"INSERT INTO {T_CON} (nb_personnes, reservation_id, voyage_id) VALUES (%s,%s,%s)",
            (nb_personnes, reservation_id, voyage_id)
        )
        _recalculer_montant(cur, reservation_id)
        conn.commit()
        return True, "Voyage ajouté à la réservation."
    except Exception as e:
        conn.rollback()
        return False, f"Erreur : {e}"
    finally:
        conn.close()

def _recalculer_montant(cur, reservation_id):
    # Montant chambres
    cur.execute(f"""
        SELECT COALESCE(SUM(ch.prix_nuit * (i.date_sortie - i.date_entree)),0) AS total
        FROM {T_INC} i
        JOIN conakry_travel_hotel_chambre ch ON i.chambre_id=ch.id
        WHERE i.reservation_id=%s
    """, (reservation_id,))
    montant_chambres = cur.fetchone()["total"] or 0

    # Montant voyages
    cur.execute(f"""
        SELECT COALESCE(SUM(v.prix * c.nb_personnes),0) AS total
        FROM {T_CON} c
        JOIN conakry_travel_hotel_voyage v ON c.voyage_id=v.id
        WHERE c.reservation_id=%s
    """, (reservation_id,))
    montant_voyages = cur.fetchone()["total"] or 0

    total = float(montant_chambres) + float(montant_voyages)
    cur.execute(f"UPDATE {T_RES} SET montant_total=%s WHERE id=%s", (total, reservation_id))

def terminer_reservation(reservation_id):
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"UPDATE {T_RES} SET statut='terminée' WHERE id=%s", (reservation_id,))
    # Libérer les chambres
    cur.execute(f"""
        UPDATE conakry_travel_hotel_chambre SET statut='disponible'
        WHERE id IN (SELECT chambre_id FROM {T_INC} WHERE reservation_id=%s)
    """, (reservation_id,))
    conn.commit()
    conn.close()
    return True, "Réservation terminée, chambres libérées."

def annuler_reservation(reservation_id):
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"UPDATE {T_RES} SET statut='annulée' WHERE id=%s", (reservation_id,))
    cur.execute(f"""
        UPDATE conakry_travel_hotel_chambre SET statut='disponible'
        WHERE id IN (SELECT chambre_id FROM {T_INC} WHERE reservation_id=%s)
    """, (reservation_id,))
    conn.commit()
    conn.close()
    return True, "Réservation annulée."

def detail_reservation(reservation_id):
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"""
        SELECT r.*, c.nom||' '||c.prenom AS client, a.nom||' '||a.prenom AS agent
        FROM {T_RES} r
        JOIN conakry_travel_hotel_client c ON r.client_id=c.id
        JOIN conakry_travel_hotel_agent  a ON r.agent_id=a.id
        WHERE r.id=%s
    """, (reservation_id,))
    res = cur.fetchone()
    cur.execute(f"""
        SELECT ch.numero, ch.type_chambre, ch.prix_nuit, i.date_entree, i.date_sortie
        FROM {T_INC} i JOIN conakry_travel_hotel_chambre ch ON i.chambre_id=ch.id
        WHERE i.reservation_id=%s
    """, (reservation_id,))
    chambres = cur.fetchall()
    cur.execute(f"""
        SELECT v.destination, v.prix, c.nb_personnes
        FROM {T_CON} c JOIN conakry_travel_hotel_voyage v ON c.voyage_id=v.id
        WHERE c.reservation_id=%s
    """, (reservation_id,))
    voyages = cur.fetchall()
    conn.close()
    return res, chambres, voyages
