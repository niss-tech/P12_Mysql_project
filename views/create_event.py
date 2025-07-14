from controllers.event_controller import create_event_for_commercial
from utils.session_user import get_current_user
from utils.session import SessionLocal
from models.contract import Contract
from models.client import Client
from datetime import datetime

def create_event_cli():
    user = get_current_user()
    if not user or user["department"] != "commercial":
        print("Seuls les commerciaux peuvent créer des événements.")
        return

    print("=== Création d’un événement ===")

    try:
        contract_id = int(input("ID du contrat signé : "))
        session = SessionLocal()

        # Vérifie que le contrat existe et appartient au commercial
        contract = session.query(Contract).filter_by(id=contract_id, sales_contact_id=user["id"]).first()
        if not contract:
            print("Contrat introuvable ou non autorisé.")
            return
        if not contract.is_signed:
            print("Ce contrat n’est pas encore signé.")
            return

        # Récupère le client lié au contrat
        client = session.query(Client).filter_by(id=contract.client_id).first()
        if not client:
            print("Client introuvable.")
            return

        print(f"\nCréation d’un événement pour : {client.full_name}")
        print(f"Email : {client.email} | Société : {client.company_name}\n")

        start_str = input("Date de début (YYYY-MM-DD HH:MM) : ")
        end_str = input("Date de fin (YYYY-MM-DD HH:MM) : ")

        data = {
            "event_date_start": datetime.strptime(start_str, "%Y-%m-%d %H:%M"),
            "event_date_end": datetime.strptime(end_str, "%Y-%m-%d %H:%M"),
            "location": input("Lieu de l’événement : "),
            "attendees": int(input("Nombre de participants : ")),
            "notes": input("Notes (optionnel) : ").strip()
        }

        success, message = create_event_for_commercial(user, contract_id, data)
        print(message if success else message)

    except ValueError:
        print("Format de date ou nombre invalide.")
    finally:
        session.close()
