import uuid
from sqlmodel import SQLModel, Field


class AdminBase(SQLModel):
    admin_email: str
    admin_password: str


class AdminLoginForm(AdminBase):
    admin_secret: str


class AdminCreateModel(AdminLoginForm):
    admin_name: str


class Admin(AdminBase, table=True):
    admin_id: int | None = Field(int, primary_key=True)
    admin_name: str
    admin_kid: str = Field(default=lambda: uuid.uuid4().hex)
