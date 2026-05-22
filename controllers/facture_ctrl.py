from database.db import get_connection, get_cursor

TABLE = "conakry_travel_hotel_facture"
T_RES = "conakry_travel_hotel_reservation"

def generer_facture(reservation_id, mode_paiement):
    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        # Vérifier si facture existe déjà
        cur.execute(f"SELECT id FROM {TABLE} WHERE reservation_id=%s", (reservation_id,))
        if cur.fetchone():
            conn.close()
            return False, "Facture déjà générée pour cette réservation.", None
        # Récupérer montant total
        cur.execute(f"SELECT montant_total FROM {T_RES} WHERE id=%s", (reservation_id,))
        res = cur.fetchone()
        if not res:
            conn.close()
            return False, "Réservation introuvable.", None
        montant = res["montant_total"]
        cur.execute(f"""
            INSERT INTO {TABLE} (date_emission, montant, statut_paiement, mode_paiement, reservation_id)
            VALUES (NOW(), %s, 'impayée', %s, %s) RETURNING id
        """, (montant, mode_paiement, reservation_id))
        facture_id = cur.fetchone()["id"]
        conn.commit()
        return True, "Facture générée.", facture_id
    except Exception as e:
        conn.rollback()
        return False, f"Erreur : {e}", None
    finally:
        conn.close()

def payer_facture(facture_id, mode_paiement=None):
    conn = get_connection()
    cur  = get_cursor(conn)
    mode = mode_paiement or "Espèces"
    cur.execute(f"""
        UPDATE {TABLE} SET statut_paiement='payée', mode_paiement=%s WHERE id=%s
    """, (mode, facture_id))
    conn.commit()
    conn.close()
    return True, "Facture marquée comme payée."

def lister_factures():
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"""
        SELECT f.id, f.date_emission, f.montant, f.statut_paiement, f.mode_paiement,
               c.nom||' '||c.prenom AS client
        FROM {TABLE} f
        JOIN {T_RES} r ON f.reservation_id=r.id
        JOIN conakry_travel_hotel_client c ON r.client_id=c.id
        ORDER BY f.date_emission DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def detail_facture(facture_id):
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"""
        SELECT f.*, c.nom||' '||c.prenom AS client, r.date_reservation, r.montant_total
        FROM {TABLE} f
        JOIN {T_RES} r ON f.reservation_id=r.id
        JOIN conakry_travel_hotel_client c ON r.client_id=c.id
        WHERE f.id=%s
    """, (facture_id,))
    row = cur.fetchone()
    conn.close()
    return row
