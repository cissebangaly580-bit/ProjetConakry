import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from views.ui import *
from views.menus import (
    vue_dashboard, vue_chambres, vue_clients, vue_agents,
    vue_reservations, vue_factures, vue_voyages
)

BANNER = f"""
{CYAN}{BOLD}
  ██╗  ██╗ ██████╗ ████████╗███████╗██╗
  ██║  ██║██╔═══██╗╚══██╔══╝██╔════╝██║
  ███████║██║   ██║   ██║   █████╗  ██║
  ██╔══██║██║   ██║   ██║   ██╔══╝  ██║
  ██║  ██║╚██████╔╝   ██║   ███████╗███████╗
  ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚══════╝
{RESET}{YELLOW}    Agence de Voyage & Hôtel — conakry_db{RESET}
{CYAN}{'═'*45}{RESET}
"""

def main():
    while True:
        clear()
        print(BANNER)
        choix = menu([
            "📊  Tableau de bord",
            "🏨  Gestion des chambres",
            "👤  Gestion des clients",
            "👷  Gestion des agents",
            "📋  Gestion des réservations",
            "🧾  Gestion des factures",
            "✈️   Gestion des voyages",
        ])
        if choix == 0:
            clear()
            print(f"\n{GREEN}{BOLD}  Au revoir !{RESET}\n")
            break
        elif choix == 1: vue_dashboard()
        elif choix == 2: vue_chambres()
        elif choix == 3: vue_clients()
        elif choix == 4: vue_agents()
        elif choix == 5: vue_reservations()
        elif choix == 6: vue_factures()
        elif choix == 7: vue_voyages()

if __name__ == "__main__":
    main()
