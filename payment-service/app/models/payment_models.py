from typing import Optional
from sqlmodel import Relationship, SQLModel, Field


class PaymentBase(SQLModel):
    order_id: int = Field(foreign_key="order.order_id")
    total_price: int
    payment_intent_id: Optional[str]
    payment_method: Optional[str]


class AdvancePaymentBase(SQLModel):
    advance_price: int
    advance_payment_intent_id: str
    advance_payment_method: str


class PaymentModel(PaymentBase):
    advance_payment: Optional[AdvancePaymentBase]


class Payment(PaymentBase, table=True):
    payment_id: int = Field(primary_key=True)
    payment_status: str
    advance_payment: Optional["AdvancePayment"] = Relationship(
        back_populates="payment")


class AdvancePayment(AdvancePaymentBase, table=True):
    advance_payment_id: Optional[int] = Field(primary_key=True)
    payment_id: int = Field(foreign_key="payment.payment_id")
    advance_payment_status: str
    payment: Optional[Payment] = Relationship(back_populates="advance_payment")
