from typing import Optional
import uuid
from sqlmodel import SQLModel, Field 
from pydantic import EmailStr

#============================================================================================================================
class UserBase(SQLModel):
    user_name: str
    phone_number: int

#============================================================================================================================    
class UserAuth(SQLModel):
    user_email: EmailStr
    user_password: str

#============================================================================================================================
class UserModel(UserAuth, UserBase):
    pass

#============================================================================================================================
class User(UserModel, table=True):
    user_id: Optional[int] = Field(int, primary_key=True)
    kid: str = Field(default=lambda:uuid.uuid4().hex)


class UserUpdateModel(SQLModel):
    user_id: int
    user_name: str | None
    user_email: str | None
    phone_number: int | None 