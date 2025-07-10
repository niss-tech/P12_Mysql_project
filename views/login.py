import json
from controllers.user_controller import authenticate_user
from utils.session_user import get_current_user


def login_cli():
    print("=== Connexion ===")
    email = input("Email : ")
    password = input("Mot de passe : ")

    user = authenticate_user(email, password)

    if user:
        # print(f" Bienvenue {user['first_name']} ({user['department']})")

        # Enregistrer l’utilisateur connecté dans un fichier session
        with open("session/session.json", "w") as f:
            json.dump(user, f)
    else:
        print(" Identifiants incorrects.")



