from controllers.client_controller import update_client_for_commercial
from utils.session_user import get_current_user

def update_client_cli():
    user = get_current_user()
    if not user or user["department"] != "commercial":
        print("Seuls les commerciaux peuvent modifier leurs clients.")
        return

    try:
        client_id = int(input("ID du client à modifier : "))

        print("Laissez vide les champs que vous ne souhaitez pas modifier.")

        new_data = {
            "full_name": input("Nouveau nom complet : ").strip() or None,
            "email": input("Nouvel email : ").strip() or None,
            "phone": input("Nouveau téléphone : ").strip() or None,
            "company_name": input("Nouveau nom de l’entreprise : ").strip() or None,
        }

        success, message = update_client_for_commercial(user["id"], client_id, new_data)
        print(message if success else message)

    except ValueError:
        print("L’ID du client doit être un nombre entier.")
