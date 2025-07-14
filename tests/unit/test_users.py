from utils.session import SessionLocal
from models.user import User
from controllers.user_controller import create_user


def test_create_user():
    session = SessionLocal()

    #Nettoyage préalable si l'utilisateur existe déjà
    session.query(User).filter_by(email="newuser@test.com").delete()
    session.commit()

    #Appel de la fonction à tester
    result = create_user(
        first_name="Alice",
        last_name="Dupont",
        email="newuser@test.com",
        password="motdepasse123",
        department_str="support"
    )

    #Vérifie que le dictionnaire retourné contient les bonnes données
    assert isinstance(result, dict)
    assert result["email"] == "newuser@test.com"
    assert result["first_name"] == "Alice"
    assert result["department"] == "support"

    #Vérifie que l'utilisateur existe bien dans la base
    user_in_db = session.query(User).filter_by(email="newuser@test.com").first()
    assert user_in_db is not None
    assert user_in_db.first_name == "Alice"


    session.delete(user_in_db)
    session.commit()
    session.close()


