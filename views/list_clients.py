from controllers.client_controller import get_all_clients
from utils.session_user import get_current_user
from controllers.client_controller import get_clients_for_commercial


def display_clients(client_list):
    if not client_list:
        print("Aucun client à afficher.")
        return

    for client in client_list:
        print(f"""
Client ID   : {client['id']}
Nom complet : {client['full_name']}
Email       : {client['email']}
Entreprise  : {client['company']}
-----------------------------""")

def list_clients_cli():
    clients = get_all_clients()
    print("\n=== TOUS LES CLIENTS (lecture seule) ===")
    display_clients(clients)


def list_my_clients_cli():
    user = get_current_user()
    if not user or user["department"] != "commercial":
        print("Seuls les commerciaux peuvent accéder à cette vue.")
        return

    clients = get_clients_for_commercial(user["id"])
    print("\n=== MES CLIENTS ASSOCIÉS ===")
    display_clients(clients)
    
# def list_clients_cli():
#     user = get_current_user()
#     if not user:
#         print("Vous devez être connecté pour voir les clients.")
#         return

#     clients = get_clients_by_user(user)

#     print(f"\nClients accessibles ({user['department']}) :")
#     display_clients(clients)