from fastapi import APIRouter, Depends
from typing import Annotated, Any
from app.controllers.custom_notification import send_custom_notification_func

router = APIRouter()

@router.post("/api/notification/send_custom_notification")
def send_custom_notification(response: Annotated[Any, Depends(send_custom_notification_func)]):
    return response
