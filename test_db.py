from config.database import engine

def test_connection():
    try:
        with engine.connect() as connection:
            print("Connexion réussie à la base de données.")
    except Exception as e:
        print("Erreur de connexion :", e)

if __name__ == "__main__":
    test_connection()
 