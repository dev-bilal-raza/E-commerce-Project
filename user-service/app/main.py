from fastapi import FastAPI
from app.routes.user_routes import user_router
from app.routes.admin_route import admin_route
from app.db.db_connector import create_db_and_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return "Welcome to User service"

app.include_router(router=user_router)
app.include_router(router=admin_route)