from database.db import get_connection, get_cursor
from datetime import date

def get_dashboard():
    conn = get_connection()
    cur  = get_cursor(conn)
    today = date.today().isoformat()

    cur.execute("SELECT COUNT(*) AS n FROM conakry_travel_hotel_chambre WHERE statut='disponible'")
    ch_libres = cur.fetchone()["n"]

    cur.execute("SELECT COUNT(*) AS n FROM conakry_travel_hotel_chambre WHERE statut='occupée'")
    ch_occupees = cur.fetchone()["n"]

    cur.execute("SELECT COUNT(*) AS n FROM conakry_travel_hotel_reservation WHERE statut='en cours'")
    res_actives = cur.fetchone()["n"]

    cur.execute("SELECT COUNT(*) AS n FROM conakry_travel_hotel_client")
    total_clients = cur.fetchone()["n"]

    cur.execute("SELECT COUNT(*) AS n FROM conakry_travel_hotel_agent")
    total_agents = cur.fetchone()["n"]

    cur.execute("SELECT COUNT(*) AS n FROM conakry_travel_hotel_voyage WHERE date_depart >= %s", (today,))
    voyages_dispo = cur.fetchone()["n"]

    cur.execute("SELECT COALESCE(SUM(montant),0) AS total FROM conakry_travel_hotel_facture WHERE statut_paiement='payée'")
    revenus = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS n FROM conakry_travel_hotel_facture WHERE statut_paiement='impayée'")
    factures_impayees = cur.fetchone()["n"]

    conn.close()
    return {
        "chambres_libres":    ch_libres,
        "chambres_occupees":  ch_occupees,
        "reservations_actives": res_actives,
        "total_clients":      total_clients,
        "total_agents":       total_agents,
        "voyages_disponibles": voyages_dispo,
        "revenus_total":      float(revenus),
        "factures_impayees":  factures_impayees,
        "date":               today,
    }
