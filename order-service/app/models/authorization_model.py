import uuid
from sqlmodel import Field, SQLModel


class Admin(SQLModel, table=True):
    admin_id: int | None = Field(int, primary_key=True)
    admin_name: str
    admin_email: str
    admin_password: str
    admin_kid: str = Field(default=lambda: uuid.uuid4().hex)