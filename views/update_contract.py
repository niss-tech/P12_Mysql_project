from utils.session_user import get_current_user
from controllers.contract_controller import update_contract

def update_contract_cli():
    user = get_current_user()

    if not user:
        print("Veuillez vous connecter.")
        return

    print("=== Modification d’un contrat ===")
    try:
        contract_id = int(input("ID du contrat à modifier : "))
        total_amount = float(input("Nouveau montant total (€) : "))
        amount_due = float(input("Nouveau montant dû (€) : "))
        is_signed_input = input("Contrat signé ? (o/n) : ").lower()
        is_signed = is_signed_input == "o"

        success, message = update_contract(contract_id, total_amount, amount_due, is_signed, user)
        print( message if success else message)

    except ValueError:
        print("Entrée invalide.")
