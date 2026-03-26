from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    email: EmailStr

class UserUpdate(BaseModel):
    """
    Modèle utilisé pour l’update partiel.
    Tous les champs sont facultatifs.
    """
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
