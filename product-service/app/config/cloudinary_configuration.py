import cloudinary  # type:ignore
from app.settings import CLOUD_NAME, CLOUD_KEY, CLOUD_SECRET


cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=CLOUD_KEY,
    api_secret=CLOUD_SECRET
)
