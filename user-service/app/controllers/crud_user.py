import json
from sqlmodel import Session, select
from app.models.user_models import User, UserModel, UserUpdateModel, UserAuth
from app.db.db_connector import DB_SESSION
from fastapi import HTTPException
from app.settings import NOTIFICATION_TOPIC
from app.utils.auth import passwordIntoHash, verifyPassword
from app.controllers.auth_user import user_login
from app.controllers.kong_controller import kong_func
from app.utils.kafka_producer import KAFKA_PRODUCER
# =================================================================================================================================


async def create_user_func(user_form: UserModel, session: DB_SESSION, producer: KAFKA_PRODUCER):
    """
    Register a new user.

    Args:
        user_name (str): The name of the user.
        user_email (str): The email of the user.
        user_password (str): The password of the user.
        session (Session): Database session.

    Raises:
        ConflictsException: Raised if the email or password already exists.

    Returns:
        dict: Data of the logged-in user.
    """
    users = session.exec(select(User))
    user_email: str = user_form.user_email
    user_password: str = user_form.user_password
    for user in users:
        password_exist = verifyPassword(user_password, user.user_password)
        if user.user_email == user_email and password_exist:
            raise HTTPException(
                status_code=404, detail="email and password already exist!")
        elif user.user_email == user_email:
            raise HTTPException(
                status_code=404, detail="This email already exist!")
        elif password_exist:
            raise HTTPException(
                status_code=404, detail="This password already exist!")
    user = add_user_in_db_func(user_form, session)
    kong_func(user.user_name, user.kid, secret_key=None)
    user_details = {
        "user_email": user_form.user_email,
        "user_password": user_form.user_password
    }
    # Login the newly registered user and return the data
    token_data = user_login(user_details=UserAuth(
        **user_details), session=session)
    print("data from login", token_data)

    message = {
        "email": user_email,
        "notification_type": "welcome_user"
    }

    # TODO: Produce message to notification topic to welcome user through email
    await producer.send_and_wait(message=json.dumps(message).encode("utf-8"), topic=NOTIFICATION_TOPIC)
    return token_data


def add_user_in_db_func(user_form: UserModel, session: Session):
    try:
        hashed_password = passwordIntoHash(user_form.user_password)
        user_form.user_password = hashed_password
        if not hashed_password:
            raise HTTPException(
                status_code=500, detail="Due to some issues, password has not convert into hashed format.")
        user = User(**user_form.model_dump())
        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return user


def get_user_by_id_func(user_id: int, session: DB_SESSION):
    user = session.get(User, user_id)
    if not user:
        HTTPException(status_code=400, detail="User not found")
    return user


def update_user_func(user_id: int, user_details: UserUpdateModel, session: DB_SESSION):
    user = session.get(User, user_id)
    if not user:
        HTTPException(status_code=400, detail="User not found")
    updated_user = user_details.model_dump(exclude_unset=True)
    for key, value in updated_user.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user_func(user_id: int, session: DB_SESSION):
    user = session.get(User, user_id)
    if not user:
        HTTPException(status_code=400, detail="User not found")

    session.delete(user)
    session.commit()
    return f"User has been successfully deleted of this id: {user_id}"
