from starlette.config import Config, EnvironError
from fastapi import HTTPException

try:
    AWS_REGION = Config().get("AWS_REGION")
    AWS_ACCESS_KEY = Config().get("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = Config().get("AWS_SECRET_KEY")
    DATABASE_URL = Config().get("DATABASE_URL")
    DOMAIN_NAME = Config().get("DOMAIN_NAME")
    USER_TOPIC = Config().get("USER_TOPIC")
    ORDER_TOPIC = Config().get("ORDER_TOPIC")
    PAYMENT_TOPIC = Config().get("PAYMENT_TOPIC")
except EnvironError as ee:
    raise HTTPException(status_code=400, detail=str(ee))