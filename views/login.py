import json
from controllers.user_controller import authenticate_user
from utils.session_user import set_current_user


def login_cli():
    print("=== Connexion ===")
    email = input("Email : ")
    password = input("Mot de passe : ")

    user = authenticate_user(email, password)

    if user:
        set_current_user(user)
        # print(f" Bienvenue {user['first_name']} ({user['department']})")

    else:
        print(" Identifiants incorrects.")



