from controllers.event_controller import get_all_events, get_events_by_support_assigned
from utils.session_user import get_current_user
from utils.session import SessionLocal
from models.client import Client
from models.user import User

def display_events(events, session):
    if not events:
        print("Aucun événement trouvé.")
        return

    for event in events:
        client = session.query(Client).filter_by(id=event.client_id).first()
        support = session.query(User).filter_by(id=event.support_contact_id).first() if event.support_contact_id else None

        print(f"""
Événement ID : {event.id}
Client           : {client.full_name if client else 'Inconnu'}
Date             : {event.event_date_start} → {event.event_date_end}
Lieu             : {event.location}
Participants     : {event.attendees}
Support          : {support.first_name + ' ' + support.last_name if support else 'Non assigné'}
Notes            : {event.notes}
-----------------------------""")

def list_events_cli():
    session = SessionLocal()
    print("=== Liste de tous les événements ===")
    try:
        events = get_all_events()
        display_events(events, session)
    finally:
        session.close()

def filter_events_by_support_cli():
    session = SessionLocal()
    print("=== Filtrage des événements ===")
    print("1. Événements avec support assigné")
    print("2. Événements sans support")
    choix = input("Choix : ")

    if choix not in ["1", "2"]:
        print("Choix invalide.")
        return

    assigned = choix == "1"
    events = get_events_by_support_assigned(assigned)
    display_events(events, session)
    session.close()
