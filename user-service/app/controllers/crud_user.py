from sqlmodel import select
from app.models.user_models import User, UserModel, UserUpdateModel
from app.db.db_connector import DB_SESSION
from fastapi import HTTPException
from app.utils.auth import passwordIntoHash, verifyPassword
from app.controllers.auth_user import user_login
from app.settings import USER_TOPIC
from app.kafka.user_producers import producer

# =================================================================================================================================
async def create_user(user_form: UserModel, session: DB_SESSION):
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
            raise HTTPException(status_code=404, detail="email and password already exist!")
        elif user.user_email == user_email:
            raise HTTPException(status_code=404, detail="This email already exist!")
        elif password_exist:
            raise HTTPException(status_code=404, detail="This password already exist!")
    await producer(message=user, topic=USER_TOPIC)

    user_details = {
        user_email: user_email,
        user_password: user_password
    }
    # Login the newly registered user and return the data
    token_data = user_login(**user_details.__dict__)
    print("data from login", token_data)
    return token_data
    

def add_user_in_db(user_form: UserModel, session: DB_SESSION):
    hashed_password = passwordIntoHash(user_form.user_password)
    user = User(**user_form.model_dump(), user_password = hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
    
def get_user(user_id: int, session: DB_SESSION):
    user = session.get(User, user_id) 
    if not user:
        HTTPException(status_code=400, detail="User not found")
    return user
    
def update_user(user_details: UserUpdateModel, session: DB_SESSION):
    user = session.get(User, user_details.user_id) 
    if not user:
        HTTPException(status_code=400, detail="User not found")
    user = user_details.model_dump(exclude_unset=True)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user():
    ...