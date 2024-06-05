from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.controllers.auth_admin import admin_verify

admin_route = APIRouter()

@admin_route.get("/admin-verify", response_model=dict[str, str])
def verify_admin(admin_token: Annotated[dict[str, str], Depends(admin_verify)]):
    if not admin_token:
        raise HTTPException(status_code=404, detail="Admin has not verified!")
    return admin_token