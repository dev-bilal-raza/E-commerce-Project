from app.utils.schemas.user_schema import welcome_message, verification_message, update_user_message
from app.utils.boto_config import send_email_via_boto


def welcome_notification_func(email: str):
    subject = "Welcome to E-commerce!"
    response = send_email_via_boto(email, subject, welcome_message)
    print(response)


def verified_notification_func(email: str):
    subject = "Your Account has been Verified"
    response = send_email_via_boto(email, subject, verification_message)
    print(response)


def user_update_notification_func(email: str):
    subject = "Your Account Details have been Updated"
    response = send_email_via_boto(email, subject, update_user_message)
    print(response)


user_notification_func_map = {
    "welcome_user": welcome_notification_func,
    "user_verification": verified_notification_func,
    "update_user_notification": user_update_notification_func,
}
