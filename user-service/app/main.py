from app.routes import admin_route, user_routes
from fastapi import FastAPI
from app.db.db_connector import create_db_and_tables
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="User and Admin Service",
    description="API for managing users",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Users", "description": "Operations with users."}
    ]
)


@app.get("/")
def home():
    return "Welcome to User service"


app.include_router(router=user_routes.router,
                   prefix="/api/v1/user", tags=["Users"])
app.include_router(router=admin_route.router,
                   prefix="/api/v1/admin", tags=["Admin"])
