from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.controllers.crud_user import create_user_func, get_user_by_id_func, update_user_func, delete_user_func
from app.controllers.auth_user import user_login
from app.models.user_models import User

router = APIRouter()


@router.get("/get_users")
def get_user(user: Annotated[User, Depends(get_user_by_id_func)]):
    return user


@router.post("/add_user")
async def add_user(token: Annotated[dict, Depends(create_user_func)]):
    if not token:
        HTTPException(
            status_code=400, detail="Try again, something occurred while generating token from library. ")
    return token


@router.post("/login_user")
async def authenticate_user(token: Annotated[dict, Depends(user_login)]):
    if not token:
        HTTPException(
            status_code=400, detail="Try again, something occurred while generating token from library. ")
    return token


@router.put("/update_user")
def update_user(updated_user: Annotated[User, Depends(update_user_func)]):
    return updated_user


@router.delete("/delete_user")
def delete_user(message: Annotated[str, Depends(delete_user_func)]):
    return message
