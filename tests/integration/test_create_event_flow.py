# tests/integration/test_create_event_flow.py

from utils.session import SessionLocal
from models.user import User
from models.contract import Contract
from models.client import Client
from models.event import Event
from controllers.client_controller import create_client
from controllers.contract_controller import create_contract
from controllers.event_controller import create_event_for_commercial
from datetime import datetime


def test_create_event_flow():
    # Création d'une session de base de données pour effectuer les opérations
    session = SessionLocal()

    # === CLEAN SETUP ===
    # On supprime d’abord les utilisateurs test au cas où ils existeraient déjà (évite les doublons)
    session.query(User).filter(User.id.in_([100, 200])).delete()
    session.commit()

    # 1. Création d’un utilisateur du département commercial
    commercial = User(
        id=100,
        first_name="Melia",
        last_name="Test",
        email="com@test.com",
        password="1234",
        department="commercial"
    )

    # 2. Création d’un utilisateur du département gestion
    gestionnaire = User(
        id=200,
        first_name="Admin",
        last_name="Gestion",
        email="gestion@test.com",
        password="admin",
        department="gestion"
    )

    # Insertion des deux utilisateurs dans la base de données
    session.add_all([commercial, gestionnaire])
    session.commit()

    # On prépare les dictionnaires simulant les utilisateurs "connectés"
    commercial_dict = {"id": 100, "department": "commercial", "email": "com@test.com"}
    gestionnaire_dict = {"id": 200, "department": "gestion", "email": "gestion@test.com"}

    # 3. Le commercial crée un client
    client = create_client({
        "full_name": "Client Test",
        "email": "client@test.com",
        "company_name": "TestCorp"
    }, current_user=commercial_dict)

    # 4. Le gestionnaire crée un contrat signé pour ce client
    success, message = create_contract(
        client_email="client@test.com",
        total_amount=1000.0,
        amount_due=200.0,
        is_signed=True,
        user=gestionnaire_dict
    )

    # Vérifie que la création du contrat s’est bien déroulée
    assert success, f"Erreur création contrat : {message}"

    # 5. On vérifie que le contrat signé existe bien en base
    contract = session.query(Contract).filter_by(client_id=client["id"], is_signed=True).first()
    assert contract is not None, "Contrat signé non trouvé."

    # 6. Le commercial crée un événement lié à ce contrat
    event_data = {
        "event_date_start": datetime(2025, 11, 1, 8, 30),  # Date et heure de début
        "event_date_end": datetime(2025, 11, 1, 20, 0),    # Date et heure de fin
        "location": "Paris",
        "attendees": 100,
        "notes": "Test Event"
    }

    # Création de l'événement
    success, message = create_event_for_commercial(
        user=commercial_dict,
        contract_id=contract.id,
        data=event_data
    )

    # Vérifie que l’événement a bien été créé
    assert success is True  # Succès attendu
    assert "succès" in message.lower()  # Le message doit contenir "succès"

    # === CLEAN-UP ===
    # Pour garder la base propre après le test, on supprime ce qui a été créé

    session.query(Event).filter_by(contract_id=contract.id).delete()
    session.query(Contract).filter_by(id=contract.id).delete()
    session.query(Client).filter_by(id=contract.client_id).delete()
    session.query(User).filter(User.id.in_([100, 200])).delete()

    session.commit()
    session.close()
