from models.client import Client
from utils.session import SessionLocal
from datetime import date


def get_all_clients():
    session = SessionLocal()
    clients = session.query(Client).all()

    client_data = []
    for client in clients:
        client_data.append({
            "id": client.id,
            "full_name": client.full_name,
            "email": client.email,
            "company": client.company_name
        })

    session.close()
    return client_data


def get_clients_for_commercial(user_id):
    session = SessionLocal()
    clients = session.query(Client).filter_by(sales_contact_id=user_id).all()

    client_data = []
    for client in clients:
        client_data.append({
            "id": client.id,
            "full_name": client.full_name,
            "email": client.email,
            "company": client.company_name
        })

    session.close()
    return client_data



def create_client(data, current_user):
    session = SessionLocal()

    # Le client est automatiquement lié au commercial connecté
    if current_user["department"] != "commercial":
        session.close()
        raise PermissionError("Seuls les commerciaux peuvent créer des clients.")

    new_client = Client(
        full_name=data["full_name"],
        email=data["email"],
        phone=data.get("phone"),
        company_name=data.get("company_name"),
        date_created=date.today(),
        last_contacted=None,
        sales_contact_id=current_user["id"]
    )

    session.add(new_client)
    session.commit()
    session.refresh(new_client)

    client_info = {
        "id": new_client.id,
        "full_name": new_client.full_name,
        "email": new_client.email,
        "company": new_client.company_name
    }

    session.close()
    return client_info



def update_client_for_commercial(user_id, client_id, new_data):
    session = SessionLocal()

    try:
        client = session.query(Client).filter_by(id=client_id, sales_contact_id=user_id).first()
        if not client:
            return False, "Client non trouvé ou non autorisé."

        # Liste des champs modifiables
        modifiables = ["full_name", "email", "phone", "company_name", "last_contacted"]

        for field in modifiables:
            if field in new_data and new_data[field] is not None:
                setattr(client, field, new_data[field])

        session.commit()
        return True, "Client mis à jour avec succès."

    except Exception as e:
        session.rollback()
        return False, f"Erreur : {e}"

    finally:
        session.close()

