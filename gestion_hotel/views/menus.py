from views.ui import *
from controllers import (
    chambre_ctrl, client_ctrl, agent_ctrl,
    reservation_ctrl, facture_ctrl, voyage_ctrl, dashboard_ctrl
)

# ══════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════════
def vue_dashboard():
    clear(); titre("TABLEAU DE BORD")
    d = dashboard_ctrl.get_dashboard()
    print(f"  📅  Date               : {BOLD}{d['date']}{RESET}")
    sep()
    print(f"  🏨  Chambres libres    : {GREEN}{BOLD}{d['chambres_libres']}{RESET}")
    print(f"  🔒  Chambres occupées  : {RED}{BOLD}{d['chambres_occupees']}{RESET}")
    print(f"  📋  Réservations actives : {CYAN}{BOLD}{d['reservations_actives']}{RESET}")
    print(f"  ✈️   Voyages disponibles : {CYAN}{BOLD}{d['voyages_disponibles']}{RESET}")
    sep()
    print(f"  👤  Total clients      : {d['total_clients']}")
    print(f"  👷  Total agents       : {d['total_agents']}")
    sep()
    print(f"  💰  Revenus totaux     : {GREEN}{BOLD}{d['revenus_total']:,.0f} GNF{RESET}")
    print(f"  ⚠️   Factures impayées  : {RED}{BOLD}{d['factures_impayees']}{RESET}")
    pause()

# ══════════════════════════════════════════════════════════════════════
#  CHAMBRES
# ══════════════════════════════════════════════════════════════════════
def vue_chambres():
    while True:
        clear(); titre("GESTION DES CHAMBRES")
        c = menu(["Voir toutes les chambres","Chambres disponibles","Chambres occupées",
                  "Ajouter une chambre","Modifier une chambre","Supprimer une chambre"])
        if c == 0: break
        elif c == 1: _show_chambres()
        elif c == 2: _show_chambres("disponible")
        elif c == 3: _show_chambres("occupée")
        elif c == 4: _add_chambre()
        elif c == 5: _edit_chambre()
        elif c == 6: _del_chambre()

def _show_chambres(statut=None):
    rows = chambre_ctrl.lister_chambres(statut)
    clear(); titre("CHAMBRES")
    if not rows: info("Aucune chambre."); pause(); return
    tableau(
        ["ID","N°","Type","Prix/nuit","Capacité","Statut"],
        [(r["id"],r["numero"],r["type_chambre"],f"{r['prix_nuit']:,.0f} GNF",
          r["capacite"],
          f"{GREEN}disponible{RESET}" if r["statut"]=="disponible" else f"{RED}{r['statut']}{RESET}")
         for r in rows], [4,6,12,14,8,12])
    pause()

def _add_chambre():
    clear(); titre("AJOUTER UNE CHAMBRE")
    numero      = saisir("Numéro")
    type_ch     = saisir("Type (Simple/Double/VIP/Suite)")
    prix        = saisir("Prix par nuit (GNF)", type_=float)
    capacite    = saisir("Capacité (nb personnes)", type_=int)
    ok, msg     = chambre_ctrl.ajouter_chambre(numero, type_ch, prix, capacite)
    succes(msg) if ok else erreur(msg); pause()

def _edit_chambre():
    clear(); titre("MODIFIER UNE CHAMBRE")
    _show_chambres()
    cid = saisir("ID chambre à modifier", type_=int)
    print(f"{YELLOW}Laissez vide pour garder la valeur actuelle.{RESET}")
    numero   = saisir("Nouveau numéro", obligatoire=False)
    type_ch  = saisir("Nouveau type",   obligatoire=False)
    prix_s   = input("  Nouveau prix : ").strip()
    prix     = float(prix_s) if prix_s else None
    cap_s    = input("  Nouvelle capacité : ").strip()
    cap      = int(cap_s) if cap_s else None
    statut   = saisir("Nouveau statut (disponible/occupée)", obligatoire=False)
    ok, msg  = chambre_ctrl.modifier_chambre(cid, numero, type_ch, prix, cap, statut)
    succes(msg) if ok else erreur(msg); pause()

def _del_chambre():
    clear(); titre("SUPPRIMER UNE CHAMBRE")
    _show_chambres()
    cid = saisir("ID chambre à supprimer", type_=int)
    if input(f"{RED}Confirmer ? (o/N) : {RESET}").strip().lower() == "o":
        ok, msg = chambre_ctrl.supprimer_chambre(cid)
        succes(msg) if ok else erreur(msg)
    else: info("Annulé.")
    pause()

# ══════════════════════════════════════════════════════════════════════
#  CLIENTS
# ══════════════════════════════════════════════════════════════════════
def vue_clients():
    while True:
        clear(); titre("GESTION DES CLIENTS")
        c = menu(["Voir tous les clients","Rechercher un client",
                  "Enregistrer un client","Modifier un client"])
        if c == 0: break
        elif c == 1: _show_clients()
        elif c == 2: _search_client()
        elif c == 3: _add_client()
        elif c == 4: _edit_client()

def _show_clients(rows=None):
    if rows is None: rows = client_ctrl.lister_clients()
    clear(); titre("CLIENTS")
    if not rows: info("Aucun client."); pause(); return
    tableau(["ID","Nom","Prénom","Email","Téléphone","Adresse"],
            [(r["id"],r["nom"],r["prenom"],r["email"] or "-",r["telephone"] or "-",r["adresse"] or "-")
             for r in rows],[4,14,14,22,14,16])
    pause()

def _search_client():
    clear(); titre("RECHERCHER UN CLIENT")
    terme = saisir("Nom / Prénom / Téléphone")
    _show_clients(client_ctrl.rechercher_client(terme))

def _add_client():
    clear(); titre("ENREGISTRER UN CLIENT")
    nom    = saisir("Nom")
    prenom = saisir("Prénom")
    email  = saisir("Email",     obligatoire=False)
    tel    = saisir("Téléphone", obligatoire=False)
    adr    = saisir("Adresse",   obligatoire=False)
    ok, msg = client_ctrl.enregistrer_client(nom, prenom, email, tel, adr)
    succes(msg) if ok else erreur(msg); pause()

def _edit_client():
    clear(); titre("MODIFIER UN CLIENT")
    _show_clients()
    cid    = saisir("ID client à modifier", type_=int)
    kwargs = {}
    for champ in ["nom","prenom","email","telephone","adresse"]:
        val = input(f"  {champ.capitalize()} (vide=inchangé) : ").strip()
        if val: kwargs[champ] = val
    ok, msg = client_ctrl.modifier_client(cid, **kwargs)
    succes(msg) if ok else erreur(msg); pause()

# ══════════════════════════════════════════════════════════════════════
#  AGENTS
# ══════════════════════════════════════════════════════════════════════
def vue_agents():
    while True:
        clear(); titre("GESTION DES AGENTS")
        c = menu(["Voir tous les agents","Ajouter un agent",
                  "Modifier un agent","Supprimer un agent"])
        if c == 0: break
        elif c == 1: _show_agents()
        elif c == 2: _add_agent()
        elif c == 3: _edit_agent()
        elif c == 4: _del_agent()

def _show_agents():
    rows = agent_ctrl.lister_agents()
    clear(); titre("AGENTS")
    if not rows: info("Aucun agent."); pause(); return
    tableau(["ID","Nom","Prénom","Login","Rôle"],
            [(r["id"],r["nom"],r["prenom"],r["login"],r["role"]) for r in rows],
            [4,14,14,16,16])
    pause()

def _add_agent():
    clear(); titre("AJOUTER UN AGENT")
    nom    = saisir("Nom")
    prenom = saisir("Prénom")
    login  = saisir("Login")
    mdp    = saisir("Mot de passe")
    role   = saisir("Rôle (admin/réceptionniste/gérant)")
    ok, msg = agent_ctrl.ajouter_agent(nom, prenom, login, mdp, role)
    succes(msg) if ok else erreur(msg); pause()

def _edit_agent():
    clear(); titre("MODIFIER UN AGENT")
    _show_agents()
    aid    = saisir("ID agent à modifier", type_=int)
    kwargs = {}
    for champ in ["nom","prenom","login","role"]:
        val = input(f"  {champ.capitalize()} (vide=inchangé) : ").strip()
        if val: kwargs[champ] = val
    mdp = input("  Nouveau mot de passe (vide=inchangé) : ").strip()
    if mdp: kwargs["mdp"] = mdp
    ok, msg = agent_ctrl.modifier_agent(aid, **kwargs)
    succes(msg) if ok else erreur(msg); pause()

def _del_agent():
    clear(); titre("SUPPRIMER UN AGENT")
    _show_agents()
    aid = saisir("ID agent à supprimer", type_=int)
    if input(f"{RED}Confirmer ? (o/N) : {RESET}").strip().lower() == "o":
        ok, msg = agent_ctrl.supprimer_agent(aid)
        succes(msg) if ok else erreur(msg)
    else: info("Annulé.")
    pause()

# ══════════════════════════════════════════════════════════════════════
#  RESERVATIONS
# ══════════════════════════════════════════════════════════════════════
def vue_reservations():
    while True:
        clear(); titre("GESTION DES RÉSERVATIONS")
        c = menu(["Voir toutes les réservations","Réservations actives",
                  "Créer une réservation","Ajouter chambre à réservation",
                  "Ajouter voyage à réservation",
                  "Terminer une réservation (check-out)","Annuler une réservation",
                  "Détail d'une réservation"])
        if c == 0: break
        elif c == 1: _show_reservations()
        elif c == 2: _show_reservations("en cours")
        elif c == 3: _creer_reservation()
        elif c == 4: _add_chambre_res()
        elif c == 5: _add_voyage_res()
        elif c == 6: _terminer_reservation()
        elif c == 7: _annuler_reservation()
        elif c == 8: _detail_reservation()

def _show_reservations(statut=None):
    rows = reservation_ctrl.lister_reservations(statut)
    clear(); titre("RÉSERVATIONS")
    if not rows: info("Aucune réservation."); pause(); return
    tableau(["ID","Date","Statut","Montant (GNF)","Client","Agent"],
            [(r["id"],str(r["date_reservation"])[:16],r["statut"],
              f"{r['montant_total']:,.0f}",r["client"],r["agent"]) for r in rows],
            [4,18,12,14,20,16])
    pause()

def _creer_reservation():
    clear(); titre("CRÉER UNE RÉSERVATION")
    _show_clients()
    client_id = saisir("ID du client", type_=int)
    _show_agents()
    agent_id  = saisir("ID de l'agent", type_=int)
    ok, msg, rid = reservation_ctrl.creer_reservation(client_id, agent_id)
    if ok: succes(msg); info(f"ID Réservation créée : {rid}")
    else: erreur(msg)
    pause()

def _add_chambre_res():
    clear(); titre("AJOUTER CHAMBRE À UNE RÉSERVATION")
    _show_reservations("en cours")
    rid = saisir("ID réservation", type_=int)
    _show_chambres("disponible")
    cid = saisir("ID chambre", type_=int)
    info("Format dates : AAAA-MM-JJ")
    d_entree = saisir("Date d'entrée")
    d_sortie = saisir("Date de sortie")
    ok, msg  = reservation_ctrl.ajouter_chambre_reservation(rid, cid, d_entree, d_sortie)
    succes(msg) if ok else erreur(msg); pause()

def _add_voyage_res():
    clear(); titre("AJOUTER VOYAGE À UNE RÉSERVATION")
    _show_reservations("en cours")
    rid = saisir("ID réservation", type_=int)
    _show_voyages()
    vid = saisir("ID voyage", type_=int)
    nb  = saisir("Nombre de personnes", type_=int)
    ok, msg = reservation_ctrl.ajouter_voyage_reservation(rid, vid, nb)
    succes(msg) if ok else erreur(msg); pause()

def _terminer_reservation():
    clear(); titre("CHECK-OUT")
    _show_reservations("en cours")
    rid = saisir("ID réservation", type_=int)
    ok, msg = reservation_ctrl.terminer_reservation(rid)
    succes(msg) if ok else erreur(msg); pause()

def _annuler_reservation():
    clear(); titre("ANNULER UNE RÉSERVATION")
    _show_reservations("en cours")
    rid = saisir("ID réservation", type_=int)
    ok, msg = reservation_ctrl.annuler_reservation(rid)
    succes(msg) if ok else erreur(msg); pause()

def _detail_reservation():
    clear(); titre("DÉTAIL RÉSERVATION")
    rid = saisir("ID réservation", type_=int)
    res, chambres, voyages = reservation_ctrl.detail_reservation(rid)
    if not res: erreur("Introuvable."); pause(); return
    sep()
    print(f"  Client      : {BOLD}{res['client']}{RESET}")
    print(f"  Agent       : {res['agent']}")
    print(f"  Date        : {str(res['date_reservation'])[:16]}")
    print(f"  Statut      : {res['statut']}")
    sep()
    if chambres:
        print(f"\n  {CYAN}Chambres :{RESET}")
        for ch in chambres:
            nuits = (ch["date_sortie"] - ch["date_entree"]).days
            print(f"    • Ch.{ch['numero']} ({ch['type_chambre']}) — {ch['date_entree']} → {ch['date_sortie']} ({nuits}n) = {float(ch['prix_nuit'])*nuits:,.0f} GNF")
    if voyages:
        print(f"\n  {CYAN}Voyages :{RESET}")
        for v in voyages:
            print(f"    • {v['destination']} x{v['nb_personnes']} pers. = {float(v['prix'])*v['nb_personnes']:,.0f} GNF")
    sep()
    print(f"  {BOLD}TOTAL : {GREEN}{float(res['montant_total']):,.0f} GNF{RESET}")
    pause()

# ══════════════════════════════════════════════════════════════════════
#  FACTURES
# ══════════════════════════════════════════════════════════════════════
def vue_factures():
    while True:
        clear(); titre("GESTION DES FACTURES")
        c = menu(["Voir toutes les factures","Générer une facture",
                  "Marquer comme payée","Détail d'une facture"])
        if c == 0: break
        elif c == 1: _show_factures()
        elif c == 2: _gen_facture()
        elif c == 3: _payer_facture()
        elif c == 4: _detail_facture()

def _show_factures():
    rows = facture_ctrl.lister_factures()
    clear(); titre("FACTURES")
    if not rows: info("Aucune facture."); pause(); return
    tableau(["ID","Date","Montant (GNF)","Statut","Mode","Client"],
            [(r["id"],str(r["date_emission"])[:10],f"{r['montant']:,.0f}",
              r["statut_paiement"],r["mode_paiement"],r["client"]) for r in rows],
            [4,12,14,10,16,20])
    pause()

def _gen_facture():
    clear(); titre("GÉNÉRER UNE FACTURE")
    _show_reservations()
    rid  = saisir("ID réservation", type_=int)
    mode = saisir("Mode de paiement (Espèces/Virement/Carte/Mobile Money)")
    ok, msg, fid = facture_ctrl.generer_facture(rid, mode)
    if ok: succes(msg); info(f"ID Facture : {fid}")
    else: erreur(msg)
    pause()

def _payer_facture():
    clear(); titre("MARQUER FACTURE COMME PAYÉE")
    _show_factures()
    fid  = saisir("ID facture", type_=int)
    mode = saisir("Mode de paiement", obligatoire=False)
    ok, msg = facture_ctrl.payer_facture(fid, mode)
    succes(msg) if ok else erreur(msg); pause()

def _detail_facture():
    clear(); titre("DÉTAIL FACTURE")
    fid = saisir("ID facture", type_=int)
    f   = facture_ctrl.detail_facture(fid)
    if not f: erreur("Facture introuvable."); pause(); return
    sep()
    print(f"  Client          : {BOLD}{f['client']}{RESET}")
    print(f"  Date émission   : {str(f['date_emission'])[:10]}")
    print(f"  Date réservation: {str(f['date_reservation'])[:16]}")
    sep()
    print(f"  Montant         : {GREEN}{BOLD}{float(f['montant']):,.0f} GNF{RESET}")
    print(f"  Statut paiement : {f['statut_paiement'].upper()}")
    print(f"  Mode paiement   : {f['mode_paiement']}")
    pause()

# ══════════════════════════════════════════════════════════════════════
#  VOYAGES
# ══════════════════════════════════════════════════════════════════════
def vue_voyages():
    while True:
        clear(); titre("GESTION DES VOYAGES")
        c = menu(["Voir tous les voyages","Ajouter un voyage",
                  "Modifier un voyage","Supprimer un voyage"])
        if c == 0: break
        elif c == 1: _show_voyages()
        elif c == 2: _add_voyage()
        elif c == 3: _edit_voyage()
        elif c == 4: _del_voyage()

def _show_voyages():
    rows = voyage_ctrl.lister_voyages()
    clear(); titre("VOYAGES")
    if not rows: info("Aucun voyage."); pause(); return
    tableau(["ID","Destination","Départ","Retour","Prix (GNF)","Places"],
            [(r["id"],r["destination"],str(r["date_depart"]),str(r["date_retour"]),
              f"{r['prix']:,.0f}",r["places_dispo"]) for r in rows],
            [4,20,12,12,14,8])
    pause()

def _add_voyage():
    clear(); titre("AJOUTER UN VOYAGE")
    dest  = saisir("Destination")
    desc  = saisir("Description", obligatoire=False)
    dep   = saisir("Date départ (AAAA-MM-JJ)")
    ret   = saisir("Date retour (AAAA-MM-JJ)")
    prix  = saisir("Prix par personne (GNF)", type_=float)
    pl    = saisir("Nombre de places disponibles", type_=int)
    ok, msg = voyage_ctrl.ajouter_voyage(dest, desc, dep, ret, prix, pl)
    succes(msg) if ok else erreur(msg); pause()

def _edit_voyage():
    clear(); titre("MODIFIER UN VOYAGE")
    _show_voyages()
    vid    = saisir("ID voyage à modifier", type_=int)
    kwargs = {}
    for champ in ["destination","description","date_depart","date_retour"]:
        val = input(f"  {champ} (vide=inchangé) : ").strip()
        if val: kwargs[champ] = val
    for champ, typ in [("prix", float),("places_dispo", int)]:
        val = input(f"  {champ} (vide=inchangé) : ").strip()
        if val: kwargs[champ] = typ(val)
    ok, msg = voyage_ctrl.modifier_voyage(vid, **kwargs)
    succes(msg) if ok else erreur(msg); pause()

def _del_voyage():
    clear(); titre("SUPPRIMER UN VOYAGE")
    _show_voyages()
    vid = saisir("ID voyage à supprimer", type_=int)
    if input(f"{RED}Confirmer ? (o/N) : {RESET}").strip().lower() == "o":
        ok, msg = voyage_ctrl.supprimer_voyage(vid)
        succes(msg) if ok else erreur(msg)
    else: info("Annulé.")
    pause()

# raccourcis internes
def _show_clients(): 
    rows = client_ctrl.lister_clients()
    clear(); titre("CLIENTS")
    if not rows: info("Aucun client."); pause(); return
    tableau(["ID","Nom","Prénom","Téléphone"],
            [(r["id"],r["nom"],r["prenom"],r["telephone"] or "-") for r in rows],[4,14,14,14])
    pause()

def _show_chambres(statut=None):
    rows = chambre_ctrl.lister_chambres(statut)
    clear(); titre("CHAMBRES")
    if not rows: info("Aucune chambre."); pause(); return
    tableau(["ID","N°","Type","Prix/nuit","Statut"],
            [(r["id"],r["numero"],r["type_chambre"],f"{r['prix_nuit']:,.0f}",r["statut"]) for r in rows],
            [4,6,12,14,12])
    pause()

def _show_reservations(statut=None):
    rows = reservation_ctrl.lister_reservations(statut)
    clear(); titre("RÉSERVATIONS")
    if not rows: info("Aucune réservation."); pause(); return
    tableau(["ID","Date","Statut","Montant","Client"],
            [(r["id"],str(r["date_reservation"])[:10],r["statut"],
              f"{r['montant_total']:,.0f}",r["client"]) for r in rows],
            [4,12,12,14,20])
    pause()
