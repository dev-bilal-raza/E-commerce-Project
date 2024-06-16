from sqlmodel import Session, select
from fastapi import HTTPException
import stripe

from app.models.order_models import Order
from app.models.payment_models import Payment, AdvancePayment, PaymentForm
from app.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def handle_booking_payment(payment_details: PaymentForm, order: Order, session: Session):
    # Ensure advance payment details are provided and valid
    advance_payment_details = payment_details.advance_payment
    if not advance_payment_details or advance_payment_details.advance_payment_method.lower().strip() == "cash on delivery":
        raise HTTPException(status_code=400, detail="Cash on delivery is not allowed for booking orders.")

    if order.advance_price != advance_payment_details.advance_price:
        raise HTTPException(status_code=400, detail="Advance payment amount does not match the order's advance price.")

    if not advance_payment_details.advance_payment_method_id:
        raise HTTPException(status_code=400, detail="Advance payment method ID is required.")

    # Create and confirm the payment intent
    payment_intent = stripe.PaymentIntent.create(
        amount=int(advance_payment_details.advance_price * 100),  # Stripe expects amount in cents
        currency="usd",
        payment_method=advance_payment_details.advance_payment_method_id,
        confirmation_method="manual",
        confirm=True
    )

    # Handle the payment intent status
    if payment_intent.status == "succeeded":
        create_advance_payment(payment_intent, order, session)
    elif payment_intent.status == "processing":
        raise HTTPException(status_code=202, detail="Payment is processing.")
    elif payment_intent.status == "canceled":
        raise HTTPException(status_code=400, detail="Payment has been canceled.")
    else:
        raise HTTPException(status_code=400, detail="Payment failed.")

def handle_ready_made_payment(payment_details: PaymentForm, order: Order, session: Session):
    # Ensure advance payment is not provided for ready-made orders
    if payment_details.advance_payment:
        raise HTTPException(status_code=400, detail="Advance payment is not applicable for ready-made orders.")

    # Handle cash on delivery and online payment methods
    if payment_details.payment_method and payment_details.payment_method.lower().strip() == "cash on delivery":
        create_cod_payment(payment_details, order, session)
    else:
        if not payment_details.payment_method_id or payment_details.total_price != order.total_price:
            raise HTTPException(status_code=400, detail="Invalid payment method ID or total price mismatch.")

        # Create and confirm the payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(payment_details.total_price * 100),  # Stripe expects amount in cents
            currency="usd",
            payment_method=payment_details.payment_method_id,
            confirmation_method="manual",
            confirm=True
        )

        # Handle the payment intent status
        if payment_intent.status == "succeeded":
            create_payment(payment_intent, order, session)
        elif payment_intent.status == "processing":
            raise HTTPException(status_code=202, detail="Payment is processing.")
        elif payment_intent.status == "canceled":
            raise HTTPException(status_code=400, detail="Payment has been canceled.")
        else:
            raise HTTPException(status_code=400, detail="Payment failed.")

def create_advance_payment(payment_intent, order, session: Session):
    # Calculate the outstanding balance and create the advance payment record
    outstanding_balance = order.total_price - order.advance_price
    advance_payment = AdvancePayment(
        advance_payment_intent_id=payment_intent.id,
        advance_payment_method=payment_intent.payment_method_types[0],
        advance_price=order.advance_price,
        advance_payment_status=payment_intent.status
    )
    payment = Payment(
        is_completed=False,
        order_id=order.order_id,
        total_price=order.total_price,
        outstanding_balance=outstanding_balance,
        payment_status="pending",
        advance_payment=advance_payment
    )
    session.add(payment)
    session.commit()
    session.refresh(payment)
    print(f"Payment Details: {payment}")

def create_cod_payment(payment_details: PaymentForm, order: Order, session: Session):
    # Create the payment record for cash on delivery
    payment = Payment(
        is_completed=False,
        order_id=order.order_id,
        total_price=order.total_price,
        payment_status="pending",
        payment_method=payment_details.payment_method
    )
    session.add(payment)
    session.commit()
    session.refresh(payment)
    print(f"Payment Details: {payment}")

def create_payment(payment_intent, order, session: Session):
    # Create the payment record for online payment
    payment = Payment(
        payment_intent_id=payment_intent.id,
        is_completed=True,
        order_id=order.order_id,
        total_price=order.total_price,
        payment_status=payment_intent.status,
        payment_method=payment_intent.payment_method_types[0]
    )
    session.add(payment)
    session.commit()
    session.refresh(payment)
    print(f"Payment Details: {payment}")

def read_payment_details(order_id: int, session: Session) -> Payment:
    payment_table = session.exec(select(Payment).where(
        Payment.order_id == order_id)).one_or_none()
    if payment_table is None:
        raise HTTPException(
            status_code=404, detail=f"Payment table not found from this order id: {order_id}")
    return payment_table


def read_advance_payment(order_id: int, session: Session) -> AdvancePayment:
    payment_table = session.exec(select(Payment).where(
        Payment.order_id == order_id)).one_or_none()
    if payment_table and payment_table.advance_payment:
        return payment_table.advance_payment
    raise HTTPException(
        status_code=404, detail=f"Advance Payment not found from this order id: {order_id}")
