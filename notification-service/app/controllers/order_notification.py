from app.utils.schemas.order_schema import (
    create_order_message, shipping_order_message, order_on_way_message, arrive_order_message,
    cancel_order_message, back_order_message
)
from app.utils.boto_config import send_email_via_boto


def order_create_notification_func(email: str):
    subject = "Your Order has been Created"
    response = send_email_via_boto(email, subject, create_order_message)
    print(response)


def order_on_ship_notification_func(email: str):
    subject = "Your Order has Shipped"
    response = send_email_via_boto(email, subject, shipping_order_message)
    print(response)


def order_on_way_notification_func(email: str):
    subject = "Your Order is on the Way"
    response = send_email_via_boto(email, subject, order_on_way_message)
    print(response)


def order_cancelled_notification_func(email: str):
    subject = "Your Order has been Cancelled"
    response = send_email_via_boto(email, subject, cancel_order_message)
    print(response)


def back_order_notification_func(email: str):
    subject = "Your Order is Backordered"
    response = send_email_via_boto(email, subject, back_order_message)
    print(response)


def order_arrive_notification_func(email: str):
    subject = "Your Order has Arrived"
    response = send_email_via_boto(email, subject, arrive_order_message)
    print(response)


order_notification_func_map = {
    "order_create_notification": order_create_notification_func,
    "order_on_ship_notification": order_on_ship_notification_func,
    "order_on_way_notification": order_on_way_notification_func,
    "order_cancelled_notification": order_cancelled_notification_func,
    "back_order_notification": back_order_notification_func,
    "order_arrive_notification": order_arrive_notification_func,
}
