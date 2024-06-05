from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.controllers.crud_user import create_user
from app.controllers.auth_user import user_login

user_router = APIRouter()

@user_router.get("/users")
def get_user():
    return "All Users"

@user_router.post("/add_user")
async def add_user(token: Annotated[dict, Depends(create_user)]):
    if not token:
        HTTPException(status_code=400, detail="Try again, something occurred while generating token from library. ")
    return token

@user_router.post("/login_user")
async def authenticate_user(token: Annotated[dict, Depends(user_login)]):
    if not token:
        HTTPException(status_code=400, detail="Try again, something occurred while generating token from library. ")
    return token

@user_router.put("/update_user")
def update_user():
    return "Update User"


@user_router.delete("/delete_user")
def delete_user():
    return "Delete User"

