from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.controllers.crud_user import create_user_func, get_user_by_id_func, update_user_func, delete_user_func
from app.controllers.auth_user import user_login
from app.models.user_models import User

user_router = APIRouter()


@user_router.get("/api/v1/users")
def get_user(user: Annotated[User, Depends(get_user_by_id_func)]):
    return user


@user_router.post("/api/v1/add_user")
async def add_user(token: Annotated[dict, Depends(create_user_func)]):
    if not token:
        HTTPException(
            status_code=400, detail="Try again, something occurred while generating token from library. ")
    return token


@user_router.post("/api/v1/login_user")
async def authenticate_user(token: Annotated[dict, Depends(user_login)]):
    if not token:
        HTTPException(
            status_code=400, detail="Try again, something occurred while generating token from library. ")
    return token


@user_router.put("/api/v1/update_user")
def update_user(updated_user: Annotated[User, Depends(update_user_func)]):
    return updated_user


@user_router.delete("/api/v1/delete_user")
def delete_user(message: Annotated[str, Depends(delete_user_func)]):
    return message
