from fastapi import HTTPException
from sqlmodel import select
from app.db.db_connector import DB_SESSION
from app.models.user_models import User, UserAuth
from app.settings import ACCESS_TOKEN_EXPIRE_TIME
from app.utils.auth import generateToken, verifyPassword


# ===============================================================================================================================
def user_login(user_details: UserAuth, session: DB_SESSION):
    print("User Details from login function: ", user_details)
    statement = select(User).where(User.user_email == user_details.user_email)
    db_user = session.exec(statement).one_or_none()

    if not db_user:
        raise HTTPException(status_code=401, detail=f"User does not exist in Database from email:{user_details.user_email}")

    is_password_exist = verifyPassword(
        user_details.user_password, db_user.user_password)

    if not is_password_exist:
        raise HTTPException(
            status_code=404, detail="User does not exist with this password!")

    # Generate JWT token
    token = generateToken(db_user, ACCESS_TOKEN_EXPIRE_TIME)
    if token:
        db_user.is_verified = True
        session.add(db_user)
        session.commit()
    return {"access_token": token, "token_type": "bearer"}

# ===============================================================================================================================
