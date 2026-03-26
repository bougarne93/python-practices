from fastapi import APIRouter, HTTPException
from app.models.user import User, UserUpdate, UserCreate, UserResponse
from app.services.user_sql_service import UserSQLService
from app.security.jwt import create_access_token
from pydantic import BaseModel, EmailStr

router = APIRouter()

@router.post("/users")
async def create_user(user: User):
    return await UserSQLService.create_user(user)


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await UserSQLService.get_user(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.get("/users")
async def get_all_users():
    return await UserSQLService.get_all_users()


@router.put("/users/{user_id}")
async def update_user(user_id: int, update: UserUpdate):
    user = await UserSQLService.update_user(user_id, update)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    ok = await UserSQLService.delete_user(user_id)
    if not ok:
        raise HTTPException(404, "User not found")
    return {"message": "User deleted"}

@router.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    return await UserSQLService.register_user(user)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/auth/login")
async def login(data: LoginRequest):
    user = await UserSQLService.authenticate(data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
