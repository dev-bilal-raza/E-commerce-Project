from sqlmodel import SQLModel, Field

class AdminBase(SQLModel):
    admin_name: str
    admin_email: str 
    admin_password: str
    admin_key: str

class AdminForm(AdminBase):
    admin_secret: str

class Admin(AdminBase, table=True):
    admin_id: int | None = Field(int, primary_key=True)
