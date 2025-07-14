# tests/unit/test_clients.py

from controllers.client_controller import create_client
from utils.session import SessionLocal
from models.client import Client


def test_create_client_by_commercial():
    
    session = SessionLocal()
    session.rollback()
    session.query(Client).filter_by(email="client@test.com").delete()
    session.commit()

    # Simule un utilisateur commercial
    user = {"id": 1, "department": "commercial", "email": "a@a.com"}

    # Données du nouveau client
    data = {
        "full_name": "Test Client",
        "email": "client@test.com",
        "company_name": "TestCorp"
    }

    # Appel de la fonction (un seul objet retourné)
    result = create_client(data, user)

    # Vérification du contenu
    assert isinstance(result, dict)
    assert result["email"] == "client@test.com"

    # Nettoyage si nécessaire
    session.query(Client).filter_by(email="client@test.com").delete()
    session.commit()
    session.close()

