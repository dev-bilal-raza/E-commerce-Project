from typing import Optional
from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    category_id: Optional[int] = Field(None, primary_key=True)
    category_name: str


class Gender(SQLModel, table=True):
    gender_id: Optional[int] = Field(None, primary_key=True)
    gender_name: str
   

class SizeCategories(SQLModel, table=True):
    size_category_id: Optional[int] = Field(None, primary_key=True)
    size_category_name: str
