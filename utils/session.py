from sqlalchemy.orm import sessionmaker
from config.database import engine


# Cette classe permet de créer une session à chaque appel
SessionLocal = sessionmaker(bind=engine)
