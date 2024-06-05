    
from sqlmodel import Field, SQLModel


class Admin(SQLModel, table=True):
    admin_id: int | None = Field(int, primary_key=True)
    admin_name: str
    admin_email: str 
    admin_password: str
    admin_key: str