import hashlib
from database.db import get_connection, get_cursor

TABLE = "conakry_travel_hotel_agent"

def hasher_mdp(mdp):
    return hashlib.sha256(mdp.encode()).hexdigest()

def lister_agents():
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"SELECT id, nom, prenom, login, role FROM {TABLE} ORDER BY nom")
    rows = cur.fetchall()
    conn.close()
    return rows

def ajouter_agent(nom, prenom, login, mdp, role):
    conn = get_connection()
    cur  = get_cursor(conn)
    try:
        cur.execute(
            f"INSERT INTO {TABLE} (nom, prenom, login, mdp_hash, role) VALUES (%s,%s,%s,%s,%s)",
            (nom, prenom, login, hasher_mdp(mdp), role)
        )
        conn.commit()
        return True, "Agent ajouté avec succès."
    except Exception as e:
        conn.rollback()
        return False, f"Erreur : {e}"
    finally:
        conn.close()

def modifier_agent(agent_id, **kwargs):
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"SELECT * FROM {TABLE} WHERE id=%s", (agent_id,))
    ag = cur.fetchone()
    if not ag:
        conn.close()
        return False, "Agent introuvable."
    mdp_hash = hasher_mdp(kwargs["mdp"]) if "mdp" in kwargs else ag["mdp_hash"]
    cur.execute(f"""
        UPDATE {TABLE} SET nom=%s, prenom=%s, login=%s, mdp_hash=%s, role=%s WHERE id=%s
    """, (
        kwargs.get("nom",    ag["nom"]),
        kwargs.get("prenom", ag["prenom"]),
        kwargs.get("login",  ag["login"]),
        mdp_hash,
        kwargs.get("role",   ag["role"]),
        agent_id
    ))
    conn.commit()
    conn.close()
    return True, "Agent modifié."

def supprimer_agent(agent_id):
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"DELETE FROM {TABLE} WHERE id=%s", (agent_id,))
    conn.commit()
    conn.close()
    return True, "Agent supprimé."

def authentifier(login, mdp):
    conn = get_connection()
    cur  = get_cursor(conn)
    cur.execute(f"SELECT * FROM {TABLE} WHERE login=%s AND mdp_hash=%s", (login, hasher_mdp(mdp)))
    agent = cur.fetchone()
    conn.close()
    return agent
