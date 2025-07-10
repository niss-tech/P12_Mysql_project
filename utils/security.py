from passlib.context import CryptContext


# Configuration du contexte de hachage
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """Renvoie un mot de passe haché avec Argon2."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie si un mot de passe correspond au hash stocké."""
    return pwd_context.verify(plain_password, hashed_password)
