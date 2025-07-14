from utils.session import SessionLocal
from models.user import User
from models.client import Client
from controllers.client_controller import create_client


def test_create_client_success():
    session = SessionLocal()

    # Nttoyage préalable 
    session.query(Client).filter_by(email="unique@test.com").delete()
    session.query(User).filter_by(id=42).delete()
    session.commit()

    # Ajout de l’utilisateur commercial en base
    test_user = User(
        id=42,
        first_name="Test",
        last_name="User",
        email="commercial@test.com",
        password="1234",
        department="commercial"
    )
    session.add(test_user)
    session.commit()

    #Simuler l'utilisateur connecté
    user = {
        "id": 42,
        "department": "commercial",
        "email": "commercial@test.com"
    }

    #Données du client
    client_data = {
        "full_name": "Client Unitaire",
        "email": "unique@test.com",
        "company_name": "TestCompagnie"
    }

    #Appel de la fonction
    result = create_client(client_data, user)

    #Vérifications
    assert isinstance(result, dict)
    assert result["email"] == "unique@test.com"
    assert result["full_name"] == "Client Unitaire"

    #Nettoyage
    created = session.query(Client).filter_by(email="unique@test.com").first()
    session.delete(created)
    session.delete(test_user)
    session.commit()
    session.close()
