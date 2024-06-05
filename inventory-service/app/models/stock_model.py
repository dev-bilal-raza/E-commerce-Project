from datetime import datetime
from typing import Literal, Optional
from sqlmodel import Relationship, SQLModel, Field 

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_name: str
    description: str
    price: float
    stock_table: "Stock" = Relationship(back_populates="product_table")

class Order(SQLModel, table=True):
    order_id: int | None = Field(int, primary_key=True)
    product_id: int = Field(int, foreign_key="product.product_id")
    user_id: int = Field(int, foreign_key="user.user_id")
    quantity: int = Field(default=1)
    created_at : datetime = Field(default=datetime.now())
    total_price: float
    
class Stock(SQLModel, table=True):
    stock_id: int | None= Field(int, primary_key=True)
    product_id: int = Field(int, foreign_key="product.product_id")
    stock : int = 0
    product_table : Product = Relationship(back_populates="stock_table")
    # stock_level: Literal["Low", "Medium", "High"] = "High" if stock> 100 else "Medium" if stock >50 else "Low"
    
    @property
    def stock_level(self) -> Literal["Low", "Medium", "High"]:
        if self.stock > 100:
            return "High"
        elif self.stock > 50:
            return "Medium"
        else:
            return "Low"
    
    