from datetime import datetime
from controllers.event_controller import update_event_by_support
from utils.session_user import get_current_user


def update_my_event_cli():
    user = get_current_user()
    if not user or user["department"] != "support":
        print("Accès refusé.")
        return

    try:
        event_id = int(input("ID de l’événement à modifier : "))
        print("Laissez vide les champs que vous ne souhaitez pas modifier.")

        start = input("Nouvelle date de début (YYYY-MM-DD HH:MM) : ").strip()
        end = input("Nouvelle date de fin (YYYY-MM-DD HH:MM) : ").strip()
        location = input("Nouveau lieu : ").strip()
        attendees = input("Nouveau nombre de participants : ").strip()
        notes = input("Nouvelles notes : ").strip()

        data = {
            "event_date_start": datetime.strptime(start, "%Y-%m-%d %H:%M") if start else None,
            "event_date_end": datetime.strptime(end, "%Y-%m-%d %H:%M") if end else None,
            "location": location or None,
            "attendees": int(attendees) if attendees else None,
            "notes": notes
        }

        success, message = update_event_by_support(user["id"], event_id, data)
        print(message if success else message)

    except ValueError:
        print("Format invalide (ID ou date ou nombre).")