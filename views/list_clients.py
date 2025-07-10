from controllers.client_controller import get_clients_by_user
from utils.session_user import get_current_user

def list_clients_cli():
    user = get_current_user()
    if not user:
        print("Vous devez être connecté pour voir les clients.")
        return

    clients = get_clients_by_user(user)

    if not clients:
        print("Aucun client visible avec votre rôle.")
        return

    print(f"Clients accessibles ({user['department']}) :\n")
    for client in clients:
        print(f"{client['full_name']} | {client['email']} | {client['company']}")
