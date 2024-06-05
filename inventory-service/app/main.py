from fastapi import FastAPI
import asyncio 
from app.db.db_connector import create_db_and_tables
from app.routes.inventory_routes import router

# async def task_initiator():
#     asyncio.create_task(user_consumer())

# async def lifespan(app: FastAPI):
#     create_db_and_tables()
#     await task_initiator()
#     yield

app = FastAPI()

@app.get("/")
def home():
    return "Welcome to Inventory service"

app.include_router(router=router)