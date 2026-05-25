from db import get_connection

def lister_voyages():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM conakry_travel_hotel_voyage ORDER BY date_depart")
    voyages = cur.fetchall()
    conn.close()
    return voyages

def ajouter_voyage(destination, description, date_depart, date_retour, prix, places_dispo):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO conakry_travel_hotel_voyage (destination, description, date_depart, date_retour, prix, places_dispo) VALUES (%s, %s, %s, %s, %s, %s)", (destination, description, date_depart, date_retour, prix, places_dispo))
    conn.commit()
    conn.close()

def modifier_voyage(id, destination, description, date_depart, date_retour, prix, places_dispo):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE conakry_travel_hotel_voyage SET destination=%s, description=%s, date_depart=%s, date_retour=%s, prix=%s, places_dispo=%s WHERE id=%s", (destination, description, date_depart, date_retour, prix, places_dispo, id))
    conn.commit()
    conn.close()

def supprimer_voyage(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM conakry_travel_hotel_voyage WHERE id=%s", (id,))
    conn.commit()
    conn.close()

def get_voyage(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM conakry_travel_hotel_voyage WHERE id=%s", (id,))
    voyage = cur.fetchone()
    conn.close()
    return voyage