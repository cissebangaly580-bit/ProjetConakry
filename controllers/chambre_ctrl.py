from database.db import get_connection, get_cursor

TABLE = "conakry_travel_hotel_chambre"

def lister_chambres(statut=None):
    conn = get_connection()
    cur  = get_cursor(conn)
    if statut:
        cur.execute(f"SELECT * FROM {TABLE} WHERE statut=%s ORDER BY numero", (statut,))
    else:
        cur.execute(f"SELECT * FROM {TABLE} ORDER BY numero")
    rows = cur.fetchall()
    conn.close()
    return rows

def ajouter_chambre(numero, type_chambre, prix_nuit, capacite, statut="disponible"):
    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        cur.execute(
            f"INSERT INTO {TABLE} (numero, type_chambre, prix_nuit, capacite, statut) VALUES (%s,%s,%s,%s,%s)",
            (numero, type_chambre, prix_nuit, capacite, statut)
        )
        conn.commit()
        return True, "Chambre ajoutée avec succès."
    except Exception as e:
        conn.rollback()
        return False, f"Erreur : {e}"
    finally:
        conn.close()

def modifier_chambre(chambre_id, numero=None, type_chambre=None, prix_nuit=None, capacite=None, statut=None):
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"SELECT * FROM {TABLE} WHERE id=%s", (chambre_id,))
    ch = cur.fetchone()
    if not ch:
        conn.close()
        return False, "Chambre introuvable."
    cur.execute(f"""
        UPDATE {TABLE} SET numero=%s, type_chambre=%s, prix_nuit=%s, capacite=%s, statut=%s WHERE id=%s
    """, (
        numero      or ch["numero"],
        type_chambre or ch["type_chambre"],
        prix_nuit   if prix_nuit is not None else ch["prix_nuit"],
        capacite    if capacite  is not None else ch["capacite"],
        statut      or ch["statut"],
        chambre_id
    ))
    conn.commit()
    conn.close()
    return True, "Chambre modifiée."

def supprimer_chambre(chambre_id):
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"DELETE FROM {TABLE} WHERE id=%s", (chambre_id,))
    conn.commit()
    conn.close()
    return True, "Chambre supprimée."

def get_chambre(chambre_id):
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"SELECT * FROM {TABLE} WHERE id=%s", (chambre_id,))
    row = cur.fetchone()
    conn.close()
    return row
