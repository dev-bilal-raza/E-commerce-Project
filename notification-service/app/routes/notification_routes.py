from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, Any
from app.utils.boto_config import verify_email_func
from app.controllers.send_notification import send_custom_notification_func, send_notification_via_template_func
from app.controllers import user_notification, payment_notification, order_notification
from app.models.email_template import EmailModel


router = APIRouter()

@router.post("/send_custom_notification")
def send_custom_notification(response: Annotated[Any, Depends(send_custom_notification_func)]):
    return response


@router.post("/verify_email")
def verify_email(response: Annotated[Any, Depends(verify_email_func)]):
    return response


@router.post("/send_user_template_notification")
def send_user_notification_via_template(email_details: EmailModel):
    try: 
        send_notification_via_template_func(email_details, user_notification.user_notification_func_map)
        return "Email sent successfully for users template."
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/send_order_template_notification")
def send_order_notification_via_template(email_details: EmailModel):
    try: 
        send_notification_via_template_func(email_details, order_notification.order_notification_func_map)
        return "Email sent successfully for orders template."
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/send_payment_template_notification")
def send_payment_notification_via_template(email_details: EmailModel):
    try: 
        send_notification_via_template_func(email_details,payment_notification.payment_notification_func_map)
        return "Email sent successfully for payment template."
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))