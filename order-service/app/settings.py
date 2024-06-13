from starlette.config import Config
from starlette.datastructures import Secret
from datetime import timedelta

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)


ADMIN_SECRET_KEY = config.get("ADMIN_SECRET_KEY")
ADMIN_EXPIRE_TIME= timedelta(minutes=int(config.get("ACCESS_TOKEN_EXPIRE_TIME")))