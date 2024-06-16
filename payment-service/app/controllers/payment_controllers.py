from sqlmodel import select
import stripe
from fastapi import HTTPException

from app.models.payment_models import AdvancePayment, Payment, PaymentForm
from app.models.order_models import Order
from app.db.db_connector import DB_SESSION
from app.controllers.payment_components import (read_payment_details, read_advance_payment,
                                                handle_ready_made_payment, handle_booking_payment)


def process_payment(payment_details: PaymentForm, session: DB_SESSION):
    # Fetch the order from the database
    order = session.get(Order, payment_details.order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order not found for order ID: {
                            payment_details.order_id}"
                            )

    try:
        # Handle booking and ready-made orders differently
        if order.order_type == "Booking":
            handle_booking_payment(payment_details, order, session)
        elif order.order_type == "Ready made":
            handle_ready_made_payment(payment_details, order, session)
        else:
            raise HTTPException(status_code=400, detail="Invalid order type.")
    except stripe.StripeError as se:
        raise HTTPException(status_code=500, detail=str(se))


def get_payment_details(order_id: int, session: DB_SESSION):
    payment_details: Payment = read_payment_details(order_id, session)
    return payment_details


def get_advance_payment_details(order_id: int, session: DB_SESSION):
    advance_payment_details: AdvancePayment = read_advance_payment(
        order_id, session)
    return advance_payment_details


def get_payment_Status(order_id: int, session: DB_SESSION):
    payment_details: Payment = read_payment_details(order_id, session)
    return {
        "order_id": payment_details.order_id,
        "payment_id": payment_details.payment_id,
        "payment_status": payment_details.payment_status
    }


def get_advance_payment_status(order_id: int, session: DB_SESSION):
    advance_payment_details: AdvancePayment = read_advance_payment(
        order_id, session)
    return {
        "order_id": order_id,
        "advance_payment_id": advance_payment_details.advance_payment_id,
        "advance_payment_status": advance_payment_details.advance_payment_status
    }


def get_payment_by_status(status: str, session: DB_SESSION):
    payment_details = session.exec(select(Payment).where(
        Payment.payment_status == status)).all()
    if payment_details:
        return payment_details
    return f"No payment details available from status: {status}."


def get_advanced_payment_by_status(status: str, session: DB_SESSION):
    advance_payment_details = session.exec(select(AdvancePayment).where(
        AdvancePayment.advance_payment_status == status)).all()
    if advance_payment_details:
        return advance_payment_details
    return f"No advance payment details available from status: {status}."


def update_payment(payment_details: dict, order_id: int, session: DB_SESSION):
    payment_table: Payment = read_payment_details(order_id, session)
    for key, value in payment_details.items():
        setattr(payment_table, key, value)
    session.add(payment_table)
    session.commit()
    session.refresh(payment_table)
    return payment_table


def update_advance_payment(advance_payment_details: dict, order_id: int, session: DB_SESSION):
    advance_payment_table: AdvancePayment = read_advance_payment(
        order_id, session)
    for key, value in advance_payment_details.items():
        setattr(advance_payment_table, key, value)
    session.add(advance_payment_table)
    session.commit()
    session.refresh(advance_payment_table)
    return advance_payment_table


def update_payment_status(status: str, order_id: int, session: DB_SESSION):
    payment_table: Payment = read_payment_details(order_id, session)
    payment_table.payment_status = status
    session.add(payment_table)
    session.commit()
    session.refresh(payment_table)
    return payment_table


def update_advance_payment_status(status: str, order_id: int, session: DB_SESSION):
    advance_payment_table: AdvancePayment = read_advance_payment(
        order_id, session)
    advance_payment_table.advance_payment_status = status
    session.add(advance_payment_table)
    session.commit()
    session.refresh(advance_payment_table)
    return advance_payment_table


def delete_payment(order_id: int, session: DB_SESSION):
    payment_table = read_payment_details(order_id, session)
    payment_table.advance_payment = None
    session.delete(payment_table)
    session.commit()
    return f"Payment has been successfully deleted for order {order_id}."
