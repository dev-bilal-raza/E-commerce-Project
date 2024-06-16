from app.models.order_models import ProductSize, Product, OrderItem, User, OrderModel, Order
from app.models.payment_models import PaymentDetails
from app.kafka.kafka_producers import producer
from sqlmodel import Session
from fastapi import HTTPException
from typing import List


def get_product_and_size(order_item: OrderItem, session: Session):
    product_size = session.get(ProductSize, order_item.product_size_id)
    product = session.get(Product, order_item.product_id)
    if not product_size:
        raise HTTPException(status_code=404, detail=f"Product size not found for id: {
                            order_item.product_size_id}"
                            )
    if not product:
        raise HTTPException(status_code=404, detail=f"Product not found for id: {
                            order_item.product_id}"
                            )
    return product_size, product

def get_user(user_id: int, session: Session) -> User:
    # Retrieve user from the database
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not user.is_verified:
        raise HTTPException(status_code=401, detail="User is not verified to create order.")
    return user

def create_order_item(order_item: OrderItem, product: Product) -> OrderItem:
    # Create an OrderItem instance
    return OrderItem(
        product_id=product.product_id,
        product_item_id=order_item.product_item_id,
        product_size_id=order_item.product_size_id,
        quantity=order_item.quantity
    )

def validate_stock(order_item: OrderItem, product_size: ProductSize):
    if order_item.quantity > product_size.stock.stock:
        raise HTTPException(status_code=400, detail=f"Quantity {
                            order_item.quantity} not available for product id: {product_size.product_size_id}"
                            )


def handle_booking_order(booking_orders: List[OrderItem], total_price: float, advance_price: float, user: User, order_details: OrderModel, payment_model: PaymentDetails, payment_details: dict, session: Session, order_responses: List[dict]):
    if payment_model.advance_payment and payment_model.advance_payment.advance_payment_method_id:
        order = Order(user_id=user.user_id,
                      order_address=order_details.order_address,
                      total_price=total_price,
                      advance_price=advance_price,
                      items=booking_orders)
        session.add(order)
        session.commit()
        session.refresh(order)
        payment_details.update({
            "order_id": order.order_id,
            "advance_price": advance_price,
            "total_price": total_price
        })
        order_responses.append({"order_id": order.order_id, "type": "Booking"})
        # Produce message to payment service with payment details
        producer(message=payment_details, topic="payment_topic")
    else:
        raise HTTPException(
            status_code=402, detail="Invalid payment credentials for booking.")


def handle_ready_made_order(ready_made_orders: List[OrderItem], total_price: float, user: User, order_details: OrderModel, payment_model: PaymentDetails, payment_details: dict, session: Session, order_responses: List[dict]):
    if payment_model.payment_method != "Cash on Delivery" and payment_model.payment_method_id:
        payment_details.update({"total_price": total_price})
    elif payment_model.payment_method == "Cash on Delivery":
        payment_details.update({"total_price": total_price})
    else:
        raise HTTPException(
            status_code=402, detail="Invalid payment credentials for ready made product.")

    order = Order(user_id=user.user_id,
                  order_address=order_details.order_address,
                  total_price=total_price,
                  items=ready_made_orders)
    session.add(order)
    session.commit()
    session.refresh(order)
    payment_details.update(
        {"order_id": order.order_id, "total_price": total_price})
    order_responses.append({"order_id": order.order_id, "type": "Ready made"})
    # Produce message to payment service with payment details
    producer(message=payment_details, topic="payment_topic")
