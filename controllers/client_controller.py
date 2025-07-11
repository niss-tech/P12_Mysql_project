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



# def get_clients_by_user(current_user):
#     session = SessionLocal()

#     if current_user["department"] == "gestion":
#         # Tous les clients
#         clients = session.query(Client).all()

#     elif current_user["department"] == "commercial":
#         # Seulement ses propres clients
#         clients = session.query(Client).filter_by(sales_contact_id=current_user["id"]).all()

#     else:
#         # Autres départements n'ont pas accès
#         clients = []

#     client_data = []
#     for client in clients:
#         client_data.append({
#             "id": client.id,
#             "full_name": client.full_name,
#             "email": client.email,
#             "company": client.company_name
#         })

#     session.close()
#     return client_data




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
