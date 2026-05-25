from db import get_connection
import hashlib

def hasher_mdp(mdp):
    return hashlib.sha256(mdp.encode()).hexdigest()

def lister_agents():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nom, prenom, login, role FROM conakry_travel_hotel_agent ORDER BY nom")
    agents = cur.fetchall()
    conn.close()
    return agents

def ajouter_agent(nom, prenom, login, mdp, role):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO conakry_travel_hotel_agent (nom, prenom, login, mdp_hash, role) VALUES (%s, %s, %s, %s, %s)", (nom, prenom, login, hasher_mdp(mdp), role))
    conn.commit()
    conn.close()

def modifier_agent(id, nom, prenom, login, role):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE conakry_travel_hotel_agent SET nom=%s, prenom=%s, login=%s, role=%s WHERE id=%s", (nom, prenom, login, role, id))
    conn.commit()
    conn.close()

def supprimer_agent(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM conakry_travel_hotel_agent WHERE id=%s", (id,))
    conn.commit()
    conn.close()

def get_agent(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nom, prenom, login, role FROM conakry_travel_hotel_agent WHERE id=%s", (id,))
    agent = cur.fetchone()
    conn.close()
    return agent

def authentifier(login, mdp):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM conakry_travel_hotel_agent WHERE login=%s AND mdp_hash=%s", (login, hasher_mdp(mdp)))
    agent = cur.fetchone()
    conn.close()
    return agent