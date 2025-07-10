from controllers.client_controller import create_client
from utils.session_user import get_current_user

def create_client_cli():
    user = get_current_user()
    if not user:
        print("Vous devez être connecté pour créer un client.")
        return

    print("=== Création d’un client ===")
    full_name = input("Nom complet : ")
    email = input("Email : ")
    phone = input("Téléphone : ")
    company = input("Nom de l’entreprise : ")

    try:
        client = create_client(
            {
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "company_name": company
            },
            current_user=user
        )
        print(f"Client {client['full_name']} enregistré avec succès.")
    except PermissionError as e:
        print(e)
