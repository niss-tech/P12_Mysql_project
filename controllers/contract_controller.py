from datetime import date
from models.contract import Contract
from models.client import Client
from utils.session import SessionLocal

def create_contract(client_email: str, total_amount: float, amount_due: float, is_signed: bool, user: dict):
    session = SessionLocal()

    try:
        if user["department"] != "gestion":
            return False, "Seuls les membres du département 'gestion' peuvent créer un contrat."

        client = session.query(Client).filter_by(email=client_email).first()

        if not client:
            return False, "Client non trouvé."

        contract = Contract(
            client_id=client.id,
            sales_contact_id=client.sales_contact_id,  # association existante
            total_amount=total_amount,
            amount_due=amount_due,
            date_created=date.today(),
            is_signed=is_signed
        )

        session.add(contract)
        session.commit()
        return True, "Contrat créé avec succès."

    except Exception as e:
        session.rollback()
        return False, f"Erreur : {e}"

    finally:
        session.close()


def update_contract(contract_id: int, total_amount: float, amount_due: float, is_signed: bool, user: dict):
    session = SessionLocal()

    try:
        contract = session.query(Contract).filter_by(id=contract_id).first()

        if not contract:
            return False, "Contrat non trouvé."

        # Seul un commercial peut modifier son propre contrat
        if user["department"] == "commercial" and contract.sales_contact_id != user["id"]:
            return False, "Vous ne pouvez modifier que vos propres contrats."

        # La gestion peut tout modifier
        if user["department"] not in ["commercial", "gestion"]:
            return False, "Vous n'avez pas l'autorisation de modifier les contrats."

        # Mise à jour des données
        contract.total_amount = total_amount
        contract.amount_due = amount_due
        contract.is_signed = is_signed

        session.commit()
        return True, "Contrat mis à jour avec succès."

    except Exception as e:
        session.rollback()
        return False, f"Erreur : {e}"

    finally:
        session.close()

def get_all_contracts():
    session = SessionLocal()
    try:
        return session.query(Contract).all()
    finally:
        session.close()



def get_contracts_by_commercial_and_status(user_id, signed, session):
    query = session.query(Contract).filter_by(sales_contact_id=user_id)
    if signed is not None:
        query = query.filter_by(is_signed=signed)
    return query.all()
