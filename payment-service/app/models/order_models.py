from sqlmodel import SQLModel, Field, Relationship
from typing import Literal, Optional, List
from datetime import datetime, timezone


class Order(SQLModel, table=True):
    order_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    order_address: str = Field(max_length=60)
    total_price: float
    advance_price: Optional[float]
    order_type: Literal["Booking", "Ready made"]
    order_status: str = Field(default="pending")
    order_date: datetime = Field(default=datetime.now(timezone.utc))
    items: List["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    order_item_id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.order_id")
    product_id: int = Field(foreign_key="product.product_id")
    product_item_id: int = Field(foreign_key="productitem.item_id")
    product_size_id: int = Field(foreign_key="productsize.product_size_id")
    quantity: int = Field(gt=0)
    order: Optional[Order] = Relationship(back_populates="items")
