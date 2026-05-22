from database.db import get_connection, get_cursor

TABLE = "conakry_travel_hotel_voyage"

def lister_voyages():
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"SELECT * FROM {TABLE} ORDER BY date_depart")
    rows = cur.fetchall()
    conn.close()
    return rows

def ajouter_voyage(destination, description, date_depart, date_retour, prix, places_dispo):
    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        cur.execute(f"""
            INSERT INTO {TABLE} (destination, description, date_depart, date_retour, prix, places_dispo)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (destination, description, date_depart, date_retour, prix, places_dispo))
        conn.commit()
        return True, "Voyage ajouté."
    except Exception as e:
        conn.rollback()
        return False, f"Erreur : {e}"
    finally:
        conn.close()

def modifier_voyage(voyage_id, **kwargs):
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"SELECT * FROM {TABLE} WHERE id=%s", (voyage_id,))
    v = cur.fetchone()
    if not v:
        conn.close()
        return False, "Voyage introuvable."
    cur.execute(f"""
        UPDATE {TABLE} SET destination=%s, description=%s, date_depart=%s,
        date_retour=%s, prix=%s, places_dispo=%s WHERE id=%s
    """, (
        kwargs.get("destination",  v["destination"]),
        kwargs.get("description",  v["description"]),
        kwargs.get("date_depart",  v["date_depart"]),
        kwargs.get("date_retour",  v["date_retour"]),
        kwargs.get("prix",         v["prix"]),
        kwargs.get("places_dispo", v["places_dispo"]),
        voyage_id
    ))
    conn.commit()
    conn.close()
    return True, "Voyage modifié."

def supprimer_voyage(voyage_id):
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"DELETE FROM {TABLE} WHERE id=%s", (voyage_id,))
    conn.commit()
    conn.close()
    return True, "Voyage supprimé."
