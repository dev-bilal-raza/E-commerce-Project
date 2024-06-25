from datetime import datetime, timezone
from typing import List, Literal, Optional
import uuid
from sqlmodel import Field, Relationship, SQLModel


class OrderItemBase(SQLModel):
    product_id: int = Field(foreign_key="product.product_id")
    product_item_id: int = Field(foreign_key="productitem.item_id")
    product_size_id: int = Field(foreign_key="productsize.product_size_id")
    quantity: int


class OrderBase(SQLModel):
    user_id: int = Field(foreign_key="user.user_id")
    order_address: str = Field(max_length=60)


class OrderModel(OrderBase):
    items: List[OrderItemBase]


class Order(OrderBase, table=True):
    order_id: Optional[int] = Field(default=None, primary_key=True)
    total_price: float
    advance_price: Optional[float]
    order_type: str
    order_status: str = Field(default="pending")
    order_date: datetime = Field(default=datetime.now(timezone.utc))

    items: List["OrderItem"] = Relationship(back_populates="order")



class OrderItem(OrderItemBase, table=True):
    order_item_id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.order_id")
    # product_id: int = Field(foreign_key="product.product_id")
    # product_item_id: int = Field(foreign_key="productitem.item_id")
    # product_size_id: int = Field(foreign_key="productsize.product_size_id")
    # quantity: int = Field(gt=0)
    order: Optional[Order] = Relationship(back_populates="items")


class ProductSize(SQLModel, table=True):
    """
    Represents a specific size of a product item.

    Attributes:
        product_size_id (Optional[int]): Primary key for ProductSize.
        size_id (int): Foreign key linking to Size.
        price (int): Price associated with this size.
        product_item_id (Optional[int]): Foreign key linking to ProductItem.
        stock (Stock): One-to-one relationship with Stock.
        product_item (Optional[ProductItem]): Many-to-one relationship with ProductItem.
    """
    product_size_id: Optional[int] = Field(None, primary_key=True)
    size_id: int = Field(foreign_key="size.size_id")
    price: int = Field(gt=0)  # Price associated with this size
    product_item_id: int= Field(foreign_key="productitem.item_id")
    # One-to-one relationship with Stock
    stock: "Stock" = Relationship(back_populates="product_size")
    product_item: Optional["ProductItem"] = Relationship(
        back_populates="sizes"
    )  # Many-to-one relationship with ProductItem


class Product(SQLModel, table=True):
    """
    Database model for products.

    Attributes:
        product_id (Optional[int]): Primary key for Product.
        category_id (int): Foreign key linking to Category.
        gender_id (int): Foreign key linking to Gender.
        product_items (List[ProductItem]): One-to-many relationship with ProductItem.
    """
    product_id: Optional[int] = Field(
        default=None, primary_key=True)  # Primary key for Product
    # category_id: int = Field(foreign_key="category.category_id")  # Foreign key linking to Category
    # gender_id: int = Field(foreign_key="gender.gender_id")  # Foreign key linking to Gender
    product_name: str  # Name of the product
    product_description: str  # Description of the product
    product_type: str
    duration: str
    advance_payment_percentage: float = Field(default=0)
    gender_id: int = Field(foreign_key="gender.gender_id")
    category_id: int = Field(foreign_key="category.category_id")
    product_items: List["ProductItem"] = Relationship(
        back_populates="product")  # One-to-many relationship with ProductItem


class ProductItem(SQLModel, table=True):
    """
    Database model for product items.

    Attributes:
        item_id (Optional[int]): Primary key for ProductItem.
        product_id (Optional[int]): Foreign key linking to Product.
        color (str): color of a product.
        image_url (str): URL of the product item image.
        product (Optional[Product]): Many-to-one relationship with Product.
        sizes (List[ProductSize]): One-to-many relationship with ProductSize.
    """
    item_id: Optional[int] = Field(
        default=None, primary_key=True)  # Primary key for ProductItem
    # Foreign key linking to Product
    product_id: int = Field(foreign_key="product.product_id")
    color: str
    # One-to-many relationship with ProductImage
    product_images: List["ProductImage"] = Relationship(
        back_populates="product_item")
    # Many-to-one relationship with Product
    product: Optional[Product] = Relationship(back_populates="product_items")
    # One-to-many relationship with ProductSize
    sizes: List[ProductSize] = Relationship(back_populates="product_item")

class ProductImage(SQLModel, table=True):
    product_image_id: Optional[int] = Field(default=None, primary_key=True)
    product_item_id: int = Field(foreign_key="productitem.item_id")
    # URL of the product item image
    product_image_url: str
    # Many-to-one relationship with ProductItem
    product_item: Optional[ProductItem] = Relationship(
        back_populates="product_images")


class Stock(SQLModel, table=True):
    """
    Database model for stock levels.

    Attributes:
        stock_id (Optional[int]): Primary key for Stock.
        product_size_id (Optional[int]): Foreign key linking to ProductSize.
        stock (int): Stock level.
        product_size (Optional[ProductSize]): One-to-one relationship with ProductSize.

    Properties:
        stock_level (Literal["Low", "Medium", "High"]): Categorizes stock level as "Low", "Medium", or "High".
    """
    stock_id: Optional[int] = Field(
        default=None, primary_key=True)  # Primary key for Stock
    product_size_id: int = Field(foreign_key="productsize.product_size_id")
    stock: int = 0  # Stock level
    product_size: Optional[ProductSize] = Relationship(
        back_populates="stock")  # One-to-one relationship with ProductSize

    @property
    def stock_level(self) -> Literal["Low", "Medium", "High"]:
        """
        Categorizes the stock level based on the quantity.

        Returns:
            Literal["Low", "Medium", "High"]: Stock level category.
        """
        if self.stock > 100:
            return "High"
        elif self.stock > 50:
            return "Medium"
        else:
            return "Low"


class User(SQLModel, table=True):
    user_id: Optional[int] = Field(int, primary_key=True)
    user_name: str
    user_email: str
    user_password: str
    country: str
    address: str = Field(max_length=60)
    phone_number: int
    is_verified: bool = Field(default=False)
    kid: str = Field(default=lambda: uuid.uuid4().hex)
