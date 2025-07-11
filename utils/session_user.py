import json
import os

SESSION_FILE = "session/session.json"

def get_current_user():
    if not os.path.exists(SESSION_FILE):
        print("Aucun utilisateur connecté.")
        return None

    try:
        with open(SESSION_FILE, "r") as f:
            user = json.load(f)
            return user  # dictionnaire : {id, email, department, etc.}
    except Exception as e:
        print(f"Erreur de lecture de la session : {e}")
        return None

def logout_user():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        print("Déconnexion réussie.")
    else:
        print("Aucun utilisateur n’était connecté.")


def set_current_user(user):
    # Enregistrer l’utilisateur connecté dans un fichier session
    os.makedirs("session", exist_ok=True)
    with open("session/session.json", "w") as f:
        json.dump(user, f)


