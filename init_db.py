from config.database import engine, Base
import models  # très important pour charger les classes !

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès !")
