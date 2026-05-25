from db import get_connection

def lister_chambres(statut=None):
    conn = get_connection()
    cur = conn.cursor()
    if statut:
        cur.execute("SELECT * FROM conakry_travel_hotel_chambre WHERE statut=%s ORDER BY numero", (statut,))
    else:
        cur.execute("SELECT * FROM conakry_travel_hotel_chambre ORDER BY numero")
    chambres = cur.fetchall()
    conn.close()
    return chambres

def ajouter_chambre(numero, type_chambre, prix_nuit, capacite, statut="disponible"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO conakry_travel_hotel_chambre (numero, type_chambre, prix_nuit, capacite, statut) VALUES (%s, %s, %s, %s, %s)", (numero, type_chambre, prix_nuit, capacite, statut))
    conn.commit()
    conn.close()

def modifier_chambre(id, numero, type_chambre, prix_nuit, capacite, statut):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE conakry_travel_hotel_chambre SET numero=%s, type_chambre=%s, prix_nuit=%s, capacite=%s, statut=%s WHERE id=%s", (numero, type_chambre, prix_nuit, capacite, statut, id))
    conn.commit()
    conn.close()

def supprimer_chambre(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM conakry_travel_hotel_chambre WHERE id=%s", (id,))
    conn.commit()
    conn.close()

def get_chambre(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM conakry_travel_hotel_chambre WHERE id=%s", (id,))
    chambre = cur.fetchone()
    conn.close()
    return chambre