import uuid
from sqlmodel import SQLModel, Field
from typing import Optional

class AdminBase(SQLModel):
    admin_email: str
    admin_password: str

class AdminLoginForm(AdminBase):
    admin_secret: str

class AdminCreateModel(AdminLoginForm):
    admin_name: str

class Admin(AdminBase, table=True):
    admin_id: Optional[int] = Field(default=None, primary_key=True)
    admin_name: str
    admin_kid: str = Field(default_factory=lambda: uuid.uuid4().hex)
