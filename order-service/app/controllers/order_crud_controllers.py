from datetime import datetime
from typing import List
from sqlmodel import select
from fastapi import HTTPException
from app.models.payment_models import PaymentDetails
from app.models.order_models import OrderModel, Order, Product
from app.controllers.order_components import (
    get_product_and_size, handle_booking_order, handle_ready_made_order, validate_stock, create_order_item, get_user)
from app.db.db_connector import DB_SESSION
from app.kafka.kafka_producers import producer


# here I have designed all controllers related to creating processes


async def create_order(order_details: OrderModel, payment_model: PaymentDetails, session: DB_SESSION):
    # Retrieve user from the database
    user = get_user(order_details.user_id, session)

    # Initialize totals and order lists
    booking_orders_total_price = 0
    booking_orders_advance_price = 0
    ready_made_orders_total_price = 0
    booking_orders = []
    ready_made_orders = []

    # Prepare the order responses and payment details
    order_responses: List[dict[str, str]] = []
    payment_details = payment_model.model_dump()

    # Process each order item
    for order_item in order_details.items:
        product_size, product = get_product_and_size(order_item, session)
        validate_stock(order_item, product_size)

        if product.product_type == "Booking":
            booking_orders_total_price += product_size.price * order_item.quantity
            booking_orders_advance_price += booking_orders_total_price * \
                product.advance_payment_percentage / 100
            item = create_order_item(order_item, product)
            booking_orders.append(item)
        elif product.product_type == "Ready made":
            item = create_order_item(order_item, product)
            ready_made_orders_total_price += product_size.price * order_item.quantity
            ready_made_orders.append(item)

    # Handle booking orders
    if len(booking_orders) > 0:
        handle_booking_order(booking_orders, booking_orders_total_price, booking_orders_advance_price,
                             user, order_details, payment_model, payment_details, session, order_responses)

    # Handle ready-made orders
    if len(ready_made_orders) > 0:
        handle_ready_made_order(ready_made_orders, ready_made_orders_total_price, user,
                                order_details, payment_model, payment_details, session, order_responses)

    # Check if there are no valid orders
    if not order_responses:
        raise HTTPException(
            status_code=400, detail="No valid order items found.")

    # Produce message to Notification service to notify user about creating order
    await producer(message={"order_responses": order_responses}, topic="notification_topic")

    return "Your order has been successfully created."


# ==============================================================================================================================

# here I have designed all controllers related to reading processes


def read_all_order(session: DB_SESSION):
    orders = session.exec(select(Order)).all()
    return orders


def read_orders_by_user(user_id: int, session: DB_SESSION):
    order_by_user = session.exec(
        select(Order).where(Order.user_id == user_id)).all()
    return order_by_user


def read_specific_product_orders(product_id: int, session: DB_SESSION):
    product_orders = []
    orders = session.exec(select(Order)).all()
    for order in orders:
        for order_item in order.items:
            if order_item.product_id == product_id:
                product = session.exec(select(Product).where(
                    Product.product_id == product_id)).one_or_none()
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
    orders_by_date = session.exec(
        select(Order).where(Order.order_status == status)).all()
    return orders_by_date


def read_specific_date_orders(date: datetime, session: DB_SESSION):
    orders_by_date = session.exec(
        select(Order).where(Order.order_date >= date)).all()
    return orders_by_date


def read_specific_type_orders(order_type: str, session: DB_SESSION):
    orders_by_date = session.exec(
        select(Order).where(Order.order_type == order_type)).all()
    return orders_by_date


# ==============================================================================================================================


# here I have designed all controllers related to updating processes
def update_order_status(order_id: int, status: str, session: DB_SESSION):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


# ==============================================================================================================================

# here I have designed all controllers related to deleting processes

def delete_order(order_id: int, session: DB_SESSION):
    order = session.exec(select(Order).where(
        Order.order_id == order_id)).one_or_none()
    session.delete(order)
    session.commit()
    return f"Order has been successfully deleted of this id: {order_id}."
