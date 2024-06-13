from datetime import datetime
from sqlmodel import select, Session
from app.models.order_models import OrderModel, OrderItem, Order, ProductSize, Product, User
from app.db.db_connector import DB_SESSION
from fastapi import HTTPException

# here I have designed all controllers related to creating processes


def create_order(order_details: OrderModel, session: DB_SESSION):
    # session.get(ProductSize, order_details.pr)
    user = session.get(User, order_details.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not user.is_verified:
        raise HTTPException(
            status_code=401, detail="You are not verified to create order.")
    for order_item in order_details.items:
        product_size = session.get(ProductSize, order_item.product_size_id)
        if not product_size:
            raise HTTPException(status_code=404, detail=f"Product size not found from this id: {
                                order_item.product_size_id}"
                                )
        if order_item.quantity > product_size.stock.stock:
            raise HTTPException(status_code=404, detail=f"{order_item.quantity} quantities is not available for this product id:{product_size.product_size_id}"
                                )
            ...
# ==============================================================================================================================

# here I have designed all controllers related to reading processes


def read_all_order(session: DB_SESSION):
    orders = session.exec(select(Order)).all()
    return orders


def read_orders_by_user(user_id: int, session: DB_SESSION):
    order_by_user = session.exec(select(Order).where(Order.user_id == user_id)).all()
    return order_by_user


def read_specific_product_orders(product_id: int, session: DB_SESSION):
    product_orders = []
    orders = session.exec(select(Order)).all()
    for order in orders:
        for order_item in order.items:
            if order_item.product_id == product_id:
                product = session.exec(select(Product).where(Product.product_id == product_id)).one_or_none()
                if product:    
                    product_orders.append(
                        {
                            "order_id": order.order_id,
                           "product_name": product.product_name,
                            "order_date": order.order_date,
                            "order_quantity": order_item.quantity, 
                        }
                    )
    return product_orders


def read_specific_status_orders(status: str, session: DB_SESSION):
    orders_by_date = session.exec(select(Order).where(Order.order_status == status)).all()
    return orders_by_date


def read_specific_date_orders(date: datetime, session: DB_SESSION):
    orders_by_date = session.exec(select(Order).where(Order.order_date>=date)).all()
    return orders_by_date
# ==============================================================================================================================


# here I have designed all controllers related to updating processes
def update_order_status():
    ...


def update_order_quantity():
    ...
# ==============================================================================================================================

# here I have designed all controllers related to deleting processes


def delete_order(order_id: int, session: DB_SESSION):
    order = session.exec(select(Order).where(Order.order_id == order_id)).one_or_none()
    session.delete(order)
    session.commit()
    return f"Order has been successfully deleted of this id: {order_id}."
    
