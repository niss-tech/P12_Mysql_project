from models.contract import Contract
from models.event import Event
from models.user import User
from models.client import Client
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



def assign_support_to_event(event_id, support_id):
    session = SessionLocal()
    try:
        event = session.query(Event).filter_by(id=event_id).first()
        if not event:
            return False, "Événement introuvable."

        support_user = session.query(User).filter_by(id=support_id, department="support").first()
        if not support_user:
            return False, "Support introuvable ou non valide."

        event.support_contact_id = support_user.id
        session.commit()
        return True, f"Support {support_user.first_name} {support_user.last_name} assigné avec succès."

    except Exception as e:
        session.rollback()
        return False, f"Erreur : {e}"
    finally:
        session.close()


def get_all_events():
    session = SessionLocal()
    events = session.query(Event).all()
    session.close()
    return events

def get_events_by_support_assigned(assigned=True):
    session = SessionLocal()
    if assigned:
        events = session.query(Event).filter(Event.support_contact_id.isnot(None)).all()
    else:
        events = session.query(Event).filter(Event.support_contact_id.is_(None)).all()
    session.close()
    return events


def get_events_for_support(support_id):
    session = SessionLocal()
    events = session.query(Event).filter_by(support_contact_id=support_id).all()
    session.close()
    return events


def update_event_by_support(support_id, event_id, data):
    session = SessionLocal()
    try:
        event = session.query(Event).filter_by(id=event_id, support_contact_id=support_id).first()
        if not event:
            return False, "Événement introuvable ou non autorisé."

        champs_modifiables = [
            "event_date_start", "event_date_end",
            "location", "attendees", "notes"
        ]

        for champ in champs_modifiables:
            if champ in data and data[champ] is not None:
                setattr(event, champ, data[champ])

        session.commit()
        return True, "Événement mis à jour avec succès."

    except Exception as e:
        session.rollback()
        return False, f"Erreur : {e}"
    finally:
        session.close()

