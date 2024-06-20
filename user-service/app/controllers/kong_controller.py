from fastapi import HTTPException
import requests  # type: ignore
from app.settings import KONG_ADMIN_URL
from typing import Optional

def kong_func(user_name: str, kid: str, secret_key: Optional[str] ):
    try:
        create_consumer_in_kong(user_name)
        create_jwt_credential_in_kong(user_name, kid, secret_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def create_consumer_in_kong(user_name: str):
    response = requests.post(
        f"{KONG_ADMIN_URL}/consumers", data={"username": user_name})
    if response.status_code != 201:
        raise HTTPException(
            status_code=500, detail="Error creating consumer in Kong")


def create_jwt_credential_in_kong(user_name: str, kid: str, secret_key: str | None):
    if secret_key:
        response = requests.post(
            f"{KONG_ADMIN_URL}/consumers/{user_name}/jwt", data={"key": kid, "secret": secret_key})
    response = requests.post(
        f"{KONG_ADMIN_URL}/consumers/{user_name}/jwt", data={"key": kid})
    if response.status_code != 201:
        raise HTTPException(
            status_code=500, detail="Error creating JWT credential in Kong")
