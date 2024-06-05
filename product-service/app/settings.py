from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)
SECRET_KEY = config.get("SECRET_KEY")
ADMIN_SECRET_KEY = config.get("ADMIN_SECRET_KEY")

CLOUD_NAME = config.get("CLOUD_NAME")
CLOUD_KEY = config.get("CLOUD_KEY")
CLOUD_SECRET = config.get("CLOUD_SECRET")