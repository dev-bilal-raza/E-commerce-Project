from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from sqlmodel import select
from app.settings import SECRET_KEY, ADMIN_SECRET_KEY
from app.db.db_connector import DB_SESSION
from app.models.admin_model import Admin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_jwt(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials")


def admin_required(token: Annotated[str, Depends(oauth2_scheme)], session: DB_SESSION):
    headers = jwt.get_unverified_headers(token)
    admin_secret = headers.get("ADMIN_SECRET_KEY")
    payload = decode_jwt(token)
    admin = session.exec(select(Admin).where(Admin.admin_name == payload.get(
        "admin_name")).where(Admin.admin_email == payload.admin_email)).one_or_none()
    if admin:
        if admin_secret == ADMIN_SECRET_KEY:
            return payload
        raise HTTPException(status_code=403, detail="Not enough permissions")
    raise HTTPException(status_code=403, detail="Not enough permissions")
