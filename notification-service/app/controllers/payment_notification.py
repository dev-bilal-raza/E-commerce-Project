from app.utils.schemas.payment_schema import payment_received_message, payment_success_message, payment_failed_message
from app.utils.boto_config import send_email_via_boto


def payment_received_notification_func(email: str):
    subject = "Payment Received"
    response = send_email_via_boto(email, subject, payment_received_message)
    print(response)


def payment_success_notification_func(email: str):
    subject = "Payment Successful"
    response = send_email_via_boto(email, subject, payment_success_message)
    print(response)


def payment_failed_notification_func(email: str):
    subject = "Payment Failed"
    response = send_email_via_boto(email, subject, payment_failed_message)
    print(response)


payment_notification_func_map = {
    "payment_received_notification": payment_received_notification_func,
    "payment_success_notification": payment_success_notification_func,
    "payment_failed_notification": payment_failed_notification_func,
}
