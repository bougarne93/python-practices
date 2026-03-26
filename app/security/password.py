import bcrypt

def hash_password(password: str) -> str:
    """
    Transforme un mot de passe en hash sécurisé.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Vérifie si le mot de passe correspond au hash stocké.
    """
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
