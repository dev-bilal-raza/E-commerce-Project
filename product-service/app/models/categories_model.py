from typing import Optional
from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    category_id: Optional[int] = Field(None, primary_key=True)
    category_name: str


class Gender(SQLModel, table=True):
    gender_id: Optional[int] = Field(None, primary_key=True)
    gender_name: str
   

class Size(SQLModel, table=True):
    """
    Represents a specific size within a size category.

    Attributes:
        size_id (Optional[int]): Primary key for Size.
        size (str | int): Size of the product (e.g., S, M, L, 8, 9).
        size_category (str): Foreign key linking to SizeCategories.
    """
    size_id: Optional[int] = Field(primary_key=True)
    size: str | int  # Size of the product (e.g., S, M, L)