from datetime import datetime, timedelta, timezone
from sqlmodel import select
from fastapi import HTTPException
from app.models.admin_model import AdminForm, Admin
from app.db.db_connector import DB_SESSION
from app.settings import ADMIN_EXPIRE_TIME, ADMIN_SECRET_KEY, ALGORITHM
from jose import jwt


def admin_verify(admin_form: AdminForm, session: DB_SESSION):
    admin_name: str = admin_form.admin_name
    admin_email: str = admin_form.admin_email
    admin_password: str = admin_form.admin_password
    admin_key: str = admin_form.admin_key

    admin = session.exec(select(Admin).where(
        (Admin.admin_name == admin_name)
        and (Admin.admin_email == admin_email)
        and (Admin.admin_password == admin_password)
        and (Admin.admin_key == admin_key)
    )).one_or_none()

    if not admin:
        HTTPException(status_code=404,
                      detail="Admin not found from this details!")
    token = generateToken(admin, admin_form.admin_secret, ADMIN_EXPIRE_TIME)

    return {
        "admin_token": token,
        "type": "bearer"
    }


def generateToken(admin: Admin, admin_secret: str, expires_delta: timedelta) -> str:
    """
    Generate a token.

    Args:
        data (dict): User data to be encoded.
        expires_delta (timedelta): Expiry time for the token.

    Returns:
        str: Generated token.
    """

    # Calculate expiry time
    expire = datetime.now(timezone.utc) + expires_delta

    payload = {
        "admin_name": admin.admin_name,
        "admin_email": admin.admin_email,
        "exp": expire
    }
    headers = {
        "kid": admin.admin_key,
        "secret": admin_secret,
    }

    # Encode token with user data and secret key
    token = jwt.encode(payload, ADMIN_SECRET_KEY,
                       algorithm=ALGORITHM, headers=headers)
    return token
