from utils.session_user import get_current_user
from utils.session import SessionLocal
from models.contract import Contract
from models.client import Client
from models.user import User
from controllers.contract_controller import get_contracts_by_commercial_and_status, get_all_contracts



def display_contracts(contracts, session, show_commercial=True):
    if not contracts:
        print("Aucun contrat trouvé.")
        return

    for contract in contracts:
        client = session.query(Client).filter_by(id=contract.client_id).first()
        line = f"""
Contrat ID : {contract.id}
Client     : {client.full_name if client else 'Inconnu'} ({client.email if client else 'N/A'})
Total      : {contract.total_amount} €
Montant dû : {contract.amount_due} €
Signé      : {'Oui' if contract.is_signed else 'Non'}
Date       : {contract.date_created}
"""
        if show_commercial:
            commercial = session.query(User).filter_by(id=contract.sales_contact_id).first()
            line += f"Commercial : {commercial.first_name} {commercial.last_name if commercial else ''}\n"

        print(line + "-----------------------------")


def list_my_contracts_cli():
    user = get_current_user()

    if not user or user["department"] != "commercial":
        print("Seuls les commerciaux peuvent accéder à cette vue.")
        return

    session = SessionLocal()
    print("\n1. Voir les contrats signés")
    print("2. Voir les contrats non signés")
    choix = input("Choix : ")

    signed = {"1": True, "2": False}.get(choix)
    if signed is None:
        print("Choix invalide.")
        return

    try:
        contrats = get_contracts_by_commercial_and_status(user["id"], signed, session)
        print("\n--- MES CONTRATS ---")
        display_contracts(contrats, session, show_commercial=False)
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        session.close()




def list_contracts_cli():
    session = SessionLocal()
    print("=== Liste des contrats (lecture seule) ===")
    try:
        contracts = get_all_contracts()
        display_contracts(contracts, session, show_commercial=True)
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        session.close()

