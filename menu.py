from views.login import login_cli
from views.logout import logout_cli
from views.create_user import create_user_cli
from views.create_client import create_client_cli
from views.list_clients import list_clients_cli, list_my_clients_cli
from views.create_contract import create_contract_cli
from views.update_contract import update_contract_cli
from views.list_contracts import list_contracts_cli, list_my_contracts_cli
from utils.session_user import get_current_user
from views.update_user import update_user_cli
from views.delete_user import delete_user_cli
from views.update_client import update_client_cli
from views.create_event import create_event_cli 

def afficher_menu(titre, actions):
    while True:
        print(f"\n--- {titre} ---")
        for key, (desc, _) in actions.items():
            print(f"{key}. {desc}")
        choix = input("Choix : ")
        action = actions.get(choix)
        if action:
            action[1]()  # exécute la fonction associée
            return choix  # retourne le choix pour que menu() puisse réagir
        else:
            print("Choix invalide.")


def menu():
    while True:
        user = get_current_user()

        if not user:
            actions = {
                "1": ("Connexion", login_cli),
                "0": ("Quitter", lambda: exit())
            }
            choix = afficher_menu("MENU NON CONNECTÉ", actions)

            #si l'utilisateur vient de se connecter, on relance la boucle
            if choix == "1":
                continue
            elif choix == "0":
                break

        # Si connecté :
        print(f"\nConnecté : {user['first_name']} ({user['department']})")
        department = user["department"]

        actions = {
            "0": ("Déconnexion", logout_cli)
        }

        if department == "gestion":
            actions.update({
                "1": ("Gérer les utilisateurs", menu_utilisateur),
                "2": ("Gérer les contrats", lambda: menu_contrat(user, can_create=True)),
                "3": ("Accéder aux ressources", menu_lecture),
                "4": ("Associer un support à un événement", lambda: print("[TODO associer support]")),
            })

        elif department == "commercial":
            actions.update({
                "1": ("Créer un client", create_client_cli),
                "2": ("Modifier mes clients", update_client_cli),
                "3": ("Voir mes clients", list_my_clients_cli),
                "4": ("Mettre à jour mes contrats", lambda: menu_contrat(user, can_create=False)),
                "5": ("Créer un événement", create_event_cli),
                "6": ("Accéder aux ressources (lecture seule)", menu_lecture),
                "7": ("Voir mes contrats", list_my_contracts_cli ),
            })

        elif department == "support":
            actions.update({
                "1": ("Voir mes événements", lambda: print("[TODO voir mes événements]")),
                "2": ("Modifier mes événements", lambda: print("[TODO modifier mes événements]")),
                "3": ("Accéder aux ressources (lecture seule)", menu_lecture),
            })

        choix = afficher_menu("MENU PRINCIPAL", actions)

        # Si on a choisi la déconnexion (clé "0")
        if choix == "0":
            continue  # retourne au début → recheck get_current_user()


def menu_utilisateur():
    actions = {
        "1": ("Créer un utilisateur", create_user_cli),
        "2": ("Modifier un utilisateur", update_user_cli),
        "3": ("Supprimer un utilisateur", delete_user_cli),
        "0": ("Retour", lambda: None)
    }
    afficher_menu("GESTION DES UTILISATEURS", actions)


def menu_contrat(user, can_create):
    actions = {
        "0": ("Retour", lambda: None),
        "1": ("Modifier un contrat", update_contract_cli),
    }
    if can_create:
        actions["2"] = ("Créer un contrat", create_contract_cli)

    afficher_menu("GESTION DES CONTRATS", actions)


def menu_lecture():
    actions = {
        "1": ("Voir les clients", list_clients_cli),
        "2": ("Voir les contrats", list_contracts_cli),
        "3": ("Voir les événements", lambda: print("[TODO voir événements]")),
        "0": ("Retour", lambda: None)
    }
    afficher_menu("RESSOURCES EN LECTURE SEULE", actions)
