from models.contract import Contract
from models.event import Event
from utils.session import SessionLocal
from datetime import datetime

def create_event_for_commercial(user, contract_id, data):
    session = SessionLocal()

    try:
        # Vérifie que le contrat appartient au commercial et est signé
        contract = session.query(Contract).filter_by(id=contract_id, sales_contact_id=user["id"]).first()
        if not contract:
            return False, "Contrat introuvable ou non autorisé."
        if not contract.is_signed:
            return False, "Ce contrat n’est pas encore signé."

        # Créer l’événement
        new_event = Event(
            client_id=contract.client_id,
            contract_id=contract.id,
            support_contact_id=None,  # à affecter plus tard
            event_date_start=data["event_date_start"],
            event_date_end=data["event_date_end"],
            location=data["location"],
            attendees=data["attendees"],
            notes=data.get("notes", "")
        )

        session.add(new_event)
        session.commit()
        return True, "Événement créé avec succès."

    except Exception as e:
        session.rollback()
        return False, f"Erreur : {e}"

    finally:
        session.close()
