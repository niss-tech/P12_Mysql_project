from models.user import User, Department
from utils.security import hash_password,verify_password
from utils.session import SessionLocal


def create_user(first_name, last_name, email, password, department_str):
    session = SessionLocal()

    # Vérifie si l'email existe déjà
    if session.query(User).filter_by(email=email).first():
        session.close()
        raise ValueError(" Un utilisateur avec cet email existe déjà.")

    try:
        department = Department(department_str)
    except ValueError:
        session.close()
        raise ValueError(" Département invalide.")

    hashed_pw = hash_password(password)

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_pw,
        department=department
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)  #  rafraîchir avant de fermer

    # Copie les données avant de fermer la session
    user_data = {
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "department": new_user.department.value,
    }

    session.close()
    return user_data


def authenticate_user(email: str, password: str):
    session = SessionLocal()
    user = session.query(User).filter_by(email=email).first()

    if user and verify_password(password, user.password):
        # Extraire les infos avant de fermer la session
        user_data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "department": user.department.value
        }
        session.close()
        return user_data

    session.close()
    return None


def update_user(user_id, new_first_name=None, new_last_name=None, new_email=None, new_department=None):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return False, "Utilisateur introuvable."

        # Dictionnaire des champs à modifier
        modifications = {
            "first_name": new_first_name,
            "last_name": new_last_name,
            "email": new_email,
            "department": new_department
        }

        for field, value in modifications.items():
            if value:  # ignore les champs vides ou None
                setattr(user, field, value)

        session.commit()
        return True, "Utilisateur mis à jour avec succès."

    except Exception as e:
        session.rollback()
        return False, f"Erreur : {e}"
    finally:
        session.close()



def delete_user(user_id):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return False, "Utilisateur introuvable."

        session.delete(user)
        session.commit()
        return True, "Utilisateur supprimé avec succès."

    except Exception as e:
        session.rollback()
        return False, f"Erreur : {e}"
    finally:
        session.close()
