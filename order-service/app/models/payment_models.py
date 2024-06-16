from typing import Optional
from sqlmodel import SQLModel


class AdvancePayment(SQLModel):
    advance_payment_method: str
    advance_payment_method_id: str


class PaymentDetails(SQLModel):
    payment_method: Optional[str]
    billing_address: str
    payment_method_id: Optional[str]
    advance_payment: Optional[AdvancePayment]
