
import sys
import os

# Ajouter le répertoire racine au path pour les imports
sys.path.append(os.getcwd())

from app.security.jwt import create_access_token
from app.core.security import SECRET_KEY, ALGORITHM
from jose import jwt

# Simuler la création d'un token
data = {"sub": "1"}
token = create_access_token(data)
print(f"Token créé: {token}")

# Tentative de décodage
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"Payload décodé: {payload}")
except Exception as e:
    print(f"Erreur lors du décodage: {e}")

from app.core.config import SECRET_KEY as sk_config
from app.security.jwt import SECRET_KEY as sk_jwt
print(f"SECRET_KEY config: {sk_config}")
print(f"SECRET_KEY jwt: {sk_jwt}")
