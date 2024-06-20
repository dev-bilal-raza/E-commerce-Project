from fastapi import FastAPI
from app.routes.user_routes import user_router
from app.routes.admin_route import admin_route
import asyncio
from app.kafka.user_consumers import user_consumer, kong_consumer
from app.db.db_connector import create_db_and_tables

async def task_initiator():
    asyncio.create_task(user_consumer())
    asyncio.create_task(kong_consumer())

async def lifespan(app: FastAPI):
    create_db_and_tables()
    await task_initiator()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return "Welcome to User service"

app.include_router(router=user_router)
app.include_router(router=admin_route)