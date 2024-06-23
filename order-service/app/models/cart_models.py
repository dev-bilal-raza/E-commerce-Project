from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class CartBase(SQLModel):
    user_id: int = Field(foreign_key="user.user_id")


class CartItemBase(SQLModel):
    quantity: int
    product_size_id: int = Field(foreign_key="productsize.product_size_id")
    product_item_id: int = Field(foreign_key="productitem.item_id")


class CartModel(CartBase, CartItemBase):
    pass


class Cart(CartBase, table=True):
    cart_id: Optional[int] = Field(default=None, primary_key=True)
    cart_items: List["CartItem"] = Relationship(back_populates="cart")


class CartItem(CartItemBase, table=True):
    cart_item_id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: int = Field(foreign_key="cart.cart_id")
    cart: Optional[Cart] = Relationship(back_populates="cart_items")


class CartUpdateModel(SQLModel):
    cart_item_id: int
    quantity: int