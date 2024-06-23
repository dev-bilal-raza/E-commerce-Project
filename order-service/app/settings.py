from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL")

SECRET_KEY = config.get("SECRET_KEY")
ADMIN_SECRET_KEY = config.get("ADMIN_SECRET_KEY")