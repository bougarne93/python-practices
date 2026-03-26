
import sys
import os
sys.path.append(os.getcwd())

from app.core import security
from app.security import jwt

print(f"Security key: {security.SECRET_KEY}")
print(f"JWT key: {jwt.SECRET_KEY}")
print(f"Security ALGORITHM: {security.ALGORITHM}")
print(f"JWT ALGORITHM: {jwt.ALGORITHM}")
