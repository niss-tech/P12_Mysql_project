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
