from starlette.config import Config
from starlette.datastructures import Secret
from datetime import timedelta

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)

# JWT settings
ALGORITHM = config.get("ALGORITHM")
SECRET_KEY = config.get("SECRET_KEY")
KONG_ADMIN_URL = config.get("KONG_ADMIN_URL")
KONG_TOPIC = config.get("KONG_TOPIC")
USER_TOPIC = config.get("USER_TOPIC")

ACCESS_TOKEN_EXPIRE_TIME= timedelta(days=int(config.get("ACCESS_TOKEN_EXPIRE_TIME")))

ADMIN_SECRET_KEY = config.get("ADMIN_SECRET_KEY")
ADMIN_EXPIRE_TIME= timedelta(minutes=int(config.get("ACCESS_TOKEN_EXPIRE_TIME")))