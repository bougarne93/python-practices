import os

# app/core/config.py

SECRET_KEY = os.getenv("SECRET_KEY", "9845621AZEDSZEA")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
