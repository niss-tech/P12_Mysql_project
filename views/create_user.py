from controllers.user_controller import create_user

def create_user_cli():
    print("=== Création d’un utilisateur ===")
    first_name = input("Prénom : ")
    last_name = input("Nom : ")
    email = input("Email : ")
    password = input("Mot de passe : ")

    print("Départements disponibles : commercial, gestion, support")
    department = input("Département : ")

    try:
        user = create_user(first_name, last_name, email, password, department)
        print(f"Utilisateur {user['first_name']} {user['last_name']} créé avec succès !")
    except ValueError as e:
        print(f"Erreur : {e}")
