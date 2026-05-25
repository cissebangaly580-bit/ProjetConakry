from db import get_connection

def lister_factures():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT f.id, f.date_emission, f.montant, f.statut_paiement, f.mode_paiement, c.nom||' '||c.prenom AS client
        FROM conakry_travel_hotel_facture f
        JOIN conakry_travel_hotel_reservation r ON f.reservation_id = r.id
        JOIN conakry_travel_hotel_client c ON r.client_id = c.id
        ORDER BY f.date_emission DESC
    """)
    factures = cur.fetchall()
    conn.close()
    return factures

def ajouter_facture(reservation_id, montant, mode_paiement):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO conakry_travel_hotel_facture (date_emission, montant, statut_paiement, mode_paiement, reservation_id) VALUES (NOW(), %s, 'impayée', %s, %s)", (montant, mode_paiement, reservation_id))
    conn.commit()
    conn.close()

def modifier_facture(id, montant, statut_paiement, mode_paiement):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE conakry_travel_hotel_facture SET montant=%s, statut_paiement=%s, mode_paiement=%s WHERE id=%s", (montant, statut_paiement, mode_paiement, id))
    conn.commit()
    conn.close()

def supprimer_facture(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM conakry_travel_hotel_facture WHERE id=%s", (id,))
    conn.commit()
    conn.close()

def get_facture(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT f.id, f.date_emission, f.montant, f.statut_paiement, f.mode_paiement, c.nom||' '||c.prenom AS client
        FROM conakry_travel_hotel_facture f
        JOIN conakry_travel_hotel_reservation r ON f.reservation_id = r.id
        JOIN conakry_travel_hotel_client c ON r.client_id = c.id
        WHERE f.id=%s
    """, (id,))
    facture = cur.fetchone()
    conn.close()
    return facture