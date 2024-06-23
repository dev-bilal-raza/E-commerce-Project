from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL")

SECRET_KEY = config.get("SECRET_KEY")
ADMIN_SECRET_KEY = config.get("ADMIN_SECRET_KEY")

AWS_REGION = config.get("AWS_REGION")
BUCKET_NAME = config.get("BUCKET_NAME")
AWS_ACCESS_KEY = config.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = config.get("AWS_SECRET_KEY")