from typing import Optional
import uuid
from sqlmodel import SQLModel, Field

# ============================================================================================================================


class UserBase(SQLModel):
    user_name: str
    country: str
    address: str = Field(max_length=60)
    phone_number: int

# ============================================================================================================================


class UserAuth(SQLModel):
    user_email: str
    user_password: str

# ============================================================================================================================


class UserModel(UserAuth, UserBase):
    pass

# ============================================================================================================================


class User(UserModel, table=True):
    user_id: Optional[int] = Field(primary_key=True)
    is_verified: bool = Field(default=False)
    kid: str = Field(default_factory=lambda: uuid.uuid4().hex)


class UserUpdateModel(SQLModel):
    user_name: str | None
    user_email: str | None
    address: str | None = Field(max_length=60)
    phone_number: int | None


class SearchHistory():
    user_id: int
    input: list[str]