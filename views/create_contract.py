from utils.session_user import get_current_user
from controllers.contract_controller import create_contract

def create_contract_cli():
    user = get_current_user()

    if not user:
        print("Veuillez vous connecter pour continuer.")
        return

    print("=== Création d’un contrat ===")
    client_email = input("Email du client : ")

    try:
        total_amount = float(input("Montant total (€) : "))
        amount_due = float(input("Montant dû (€) : "))
        is_signed_input = input("Contrat signé ? (o/n) : ").lower()
        is_signed = is_signed_input == "o"

        success, message = create_contract(client_email, total_amount, amount_due, is_signed, user)

        if success:
            print(f"\n {message}")
        else:
            print(f"\n {message}")

    except ValueError:
        print("Montant invalide. Veuillez entrer un nombre.")
