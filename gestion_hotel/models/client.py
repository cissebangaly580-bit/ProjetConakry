from db import get_connection

def lister_clients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM conakry_travel_hotel_client ORDER BY nom")
    clients = cur.fetchall()
    conn.close()
    return clients

def ajouter_client(nom, prenom, email, telephone, adresse):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO conakry_travel_hotel_client (nom, prenom, email, telephone, adresse) VALUES (%s, %s, %s, %s, %s)", (nom, prenom, email, telephone, adresse))
    conn.commit()
    conn.close()

def modifier_client(id, nom, prenom, email, telephone, adresse):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE conakry_travel_hotel_client SET nom=%s, prenom=%s, email=%s, telephone=%s, adresse=%s WHERE id=%s", (nom, prenom, email, telephone, adresse, id))
    conn.commit()
    conn.close()

def supprimer_client(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM conakry_travel_hotel_client WHERE id=%s", (id,))
    conn.commit()
    conn.close()

def get_client(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM conakry_travel_hotel_client WHERE id=%s", (id,))
    client = cur.fetchone()
    conn.close()
    return client

def rechercher_client(terme):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM conakry_travel_hotel_client WHERE nom ILIKE %s OR prenom ILIKE %s OR telephone ILIKE %s", (f"%{terme}%",)*3)
    clients = cur.fetchall()
    conn.close()
    return clients