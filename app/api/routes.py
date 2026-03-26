from typing import List
from fastapi import APIRouter, HTTPException, Query
from app.models.user import User, UserUpdate
from app.services.user_service import UserService

router = APIRouter()

@router.get("/hello")
def say_hello():
    return {"message": "Hello Mohamed, your Python backend is ready!"}

@router.post("/users")
def create_user(users: List[User]):
    """
    Endpoint HTTP POST pour créer un utilisateur.
    """
    created = []
    for u in users:
        created_user = UserService.create_user(u)
        created.append(created_user)

    return {"status": "success", "users": created}

@router.get("/users")
def get_users(ids: List[int] = Query(...)):
    """
    Endpoint HTTP GET pour récupérer un utilisateur par ID.
    """
    display_users = []
    for user_id in ids:
        user = UserService.get_user(user_id)

        if not user:
            # FastAPI permet de renvoyer facilement une erreur 404
            raise HTTPException(
                status_code=404,
                detail=f"User with ID {user_id} not found"
            )

        display_users.append(user)

    return {"status": "success", "users": display_users}

@router.get("/users/all")
def get_all_users():
    users = UserService.get_all_users()
    return {"status": "success", "users": users}

@router.put("/users/{user_id}")
def update_user(user_id: int, update: UserUpdate):
    updated = UserService.update_user(user_id, update)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found"
        )

    return {"status": "success", "user": updated}

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    deleted = UserService.delete_user(user_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found"
        )

    return {"status": "success", "message": f"User {user_id} deleted"}
