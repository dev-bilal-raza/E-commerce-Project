from fastapi import FastAPI
from app.routes.notification_routes import router
from app.tasks.background_tasks import notification_tasks

async def lifespan(app: FastAPI):
    await notification_tasks()
    yield

app = FastAPI(lifespan=lifespan)

@app.get('/api/notification')
def home():
    return "Welcome to the Notification Service!"

app.include_router(router=router)