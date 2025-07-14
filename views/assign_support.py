from controllers.event_controller import assign_support_to_event
from utils.session_user import get_current_user

def assign_support_cli():
    user = get_current_user()
    if not user or user["department"] != "gestion":
        print("Seuls les utilisateurs du département 'gestion' peuvent effectuer cette action.")
        return

    print("=== Association d’un support à un événement ===")
    try:
        event_id = int(input("ID de l’événement à modifier : "))
        support_id = int(input("ID du support à assigner : "))

        success, message = assign_support_to_event(event_id, support_id)
        print(message if success else message)

    except ValueError:
        print("ID invalide : Veuillez entrer des nombres entiers.")
