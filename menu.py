from views.login import login_cli
from views.logout import logout_cli
from views.create_user import create_user_cli
from views.create_client import create_client_cli
from views.list_clients import list_clients_cli
from utils.session_user import get_current_user

# TODO: importer les autres vues au fur et à mesure

def menu():
    while True:
        user = get_current_user()

        if not user:
            print("1. Connexion")
            print("0. Quitter")
            choix = input("Choix : ")

            if choix == "1":
                login_cli()
            elif choix == "0":
                print(" À bientôt !")
                break
            else:
                print(" Choix invalide.")
            continue

        print(f"\n Connecté : {user['first_name']} ({user['department']})")

        department = user["department"]
        actions = {"0": ("Déconnexion", logout_cli)}  # commun à tous

        if department == "gestion":
            actions.update({
                "1": ("Créer un utilisateur", lambda: print("[TODO créer utilisateur]")),
                "2": ("Modifier un utilisateur", lambda: print("[TODO modifier utilisateur]")),
                "3": ("Supprimer un utilisateur", lambda: print("[TODO supprimer utilisateur]")),
                "4": ("Voir tous les clients", list_clients_cli),
                "5": ("Créer / Modifier un contrat", lambda: print("[TODO contrat gestion]")),
                "6": ("Voir tous les événements", lambda: print("[TODO voir tous événements]")),
                "7": ("Associer un support à un événement", lambda: print("[TODO associer support]")),
            })

        elif department == "commercial":
            actions.update({
                "1": ("Créer un client", create_client_cli),
                "2": ("Modifier mes clients", lambda: print("[TODO modifier mes clients]")),
                "3": ("Créer un contrat", lambda: print("[TODO créer contrat]")),
                "4": ("Modifier mes contrats", lambda: print("[TODO modifier contrats]")),
                "5": ("Créer un événement (client avec contrat signé)", lambda: print("[TODO créer événement]")),
                "6": ("Voir tous les clients / contrats / événements", lambda: print("[TODO affichage général]")),
            })

        elif department == "support":
            actions.update({
                "1": ("Voir mes événements", lambda: print("[TODO voir mes événements]")),
                "2": ("Modifier mes événements", lambda: print("[TODO modifier mes événements]")),
                "3": ("Voir tous les événements", lambda: print("[TODO voir tous événements]")),
            })

        print("\n === Menu principal ===")
        for key, (desc, _) in actions.items():
            print(f"{key}. {desc}")

        choix = input("Choix : ")
        action = actions.get(choix)

        if action:
            action[1]()
        else:
            print(" Choix invalide.")
