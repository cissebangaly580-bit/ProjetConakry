import os

RESET   = "\033[0m";  BOLD    = "\033[1m"
CYAN    = "\033[96m"; GREEN   = "\033[92m"
RED     = "\033[91m"; YELLOW  = "\033[93m"
BLUE    = "\033[94m"; WHITE   = "\033[97m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def titre(texte):
    ligne = "═" * (len(texte) + 4)
    print(f"\n{CYAN}{BOLD}╔{ligne}╗")
    print(f"║  {WHITE}{texte}{CYAN}  ║")
    print(f"╚{ligne}╝{RESET}\n")

def succes(msg):  print(f"{GREEN}✔  {msg}{RESET}")
def erreur(msg):  print(f"{RED}✘  {msg}{RESET}")
def info(msg):    print(f"{YELLOW}ℹ  {msg}{RESET}")
def sep():        print(f"{CYAN}{'─'*58}{RESET}")

def menu(options):
    sep()
    for i, opt in enumerate(options, 1):
        print(f"  {CYAN}{BOLD}{i:2}.{RESET} {opt}")
    print(f"  {CYAN}{BOLD} 0.{RESET} ← Retour / Quitter")
    sep()
    while True:
        try:
            c = int(input(f"{YELLOW}Votre choix : {RESET}"))
            if 0 <= c <= len(options):
                return c
        except ValueError:
            pass
        erreur("Choix invalide.")

def saisir(label, obligatoire=True, type_=str, defaut=None):
    hint = f" [{defaut}]" if defaut is not None else (" *" if obligatoire else "")
    while True:
        val = input(f"  {label}{hint} : ").strip()
        if not val and defaut is not None: return defaut
        if not val and obligatoire: erreur("Champ obligatoire."); continue
        if not val: return None
        try: return type_(val)
        except ValueError: erreur(f"Valeur invalide.")

def tableau(colonnes, lignes, largeurs=None):
    if not largeurs:
        largeurs = [max(len(str(c)), max((len(str(l[i])) for l in lignes), default=0))
                    for i, c in enumerate(colonnes)]
    s = "+" + "+".join("-"*(w+2) for w in largeurs) + "+"
    h = "|" + "|".join(f" {CYAN}{BOLD}{c:<{w}}{RESET} " for c,w in zip(colonnes,largeurs)) + "|"
    print(s); print(h); print(s)
    for l in lignes:
        print("|" + "|".join(f" {str(v):<{w}} " for v,w in zip(l,largeurs)) + "|")
    print(s)
    print(f"{YELLOW}  {len(lignes)} enregistrement(s){RESET}\n")

def pause():
    input(f"\n{CYAN}Appuyez sur Entrée pour continuer...{RESET}")
