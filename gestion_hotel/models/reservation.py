from db import get_connection

def lister_reservations():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.id, r.date_reservation, r.statut, r.montant_total,
               c.nom||' '||c.prenom AS client,
               a.nom||' '||a.prenom AS agent
        FROM conakry_travel_hotel_reservation r
        JOIN conakry_travel_hotel_client c ON r.client_id = c.id
        JOIN conakry_travel_hotel_agent a ON r.agent_id = a.id
        ORDER BY r.date_reservation DESC
    """)
    reservations = cur.fetchall()
    conn.close()
    return reservations

def ajouter_reservation(client_id, agent_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO conakry_travel_hotel_reservation 
        (date_reservation, statut, montant_total, client_id, agent_id) 
        VALUES (NOW(), 'en cours', 0, %s, %s)
        RETURNING id
    """, (client_id, agent_id))
    res_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return res_id
def modifier_reservation(id, statut):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE conakry_travel_hotel_reservation 
        SET statut=%s
        WHERE id=%s
    """, (statut, id))
    conn.commit()
    conn.close()

def supprimer_reservation(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM conakry_travel_hotel_reservation WHERE id=%s", (id,))
    conn.commit()
    conn.close()

def get_reservation(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.id, r.date_reservation, r.statut, r.montant_total,
               c.nom||' '||c.prenom AS client,
               a.nom||' '||a.prenom AS agent
        FROM conakry_travel_hotel_reservation r
        JOIN conakry_travel_hotel_client c ON r.client_id = c.id
        JOIN conakry_travel_hotel_agent a ON r.agent_id = a.id
        WHERE r.id=%s
    """, (id,))
    reservation = cur.fetchone()
    conn.close()
    return reservation