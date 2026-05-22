from database.db import get_connection, get_cursor

TABLE = "conakry_travel_hotel_client"

def lister_clients():
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"SELECT * FROM {TABLE} ORDER BY nom")
    rows = cur.fetchall()
    conn.close()
    return rows

def enregistrer_client(nom, prenom, email, telephone, adresse):
    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        cur.execute(
            f"INSERT INTO {TABLE} (nom, prenom, email, telephone, adresse) VALUES (%s,%s,%s,%s,%s)",
            (nom, prenom, email, telephone, adresse)
        )
        conn.commit()
        return True, "Client enregistré avec succès."
    except Exception as e:
        conn.rollback()
        return False, f"Erreur : {e}"
    finally:
        conn.close()

def modifier_client(client_id, **kwargs):
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"SELECT * FROM {TABLE} WHERE id=%s", (client_id,))
    cl = cur.fetchone()
    if not cl:
        conn.close()
        return False, "Client introuvable."
    cur.execute(f"""
        UPDATE {TABLE} SET nom=%s, prenom=%s, email=%s, telephone=%s, adresse=%s WHERE id=%s
    """, (
        kwargs.get("nom",       cl["nom"]),
        kwargs.get("prenom",    cl["prenom"]),
        kwargs.get("email",     cl["email"]),
        kwargs.get("telephone", cl["telephone"]),
        kwargs.get("adresse",   cl["adresse"]),
        client_id
    ))
    conn.commit()
    conn.close()
    return True, "Client modifié."

def rechercher_client(terme):
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"""
        SELECT * FROM {TABLE}
        WHERE nom ILIKE %s OR prenom ILIKE %s OR telephone ILIKE %s
    """, (f"%{terme}%",)*3)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_client(client_id):
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"SELECT * FROM {TABLE} WHERE id=%s", (client_id,))
    row = cur.fetchone()
    conn.close()
    return row
