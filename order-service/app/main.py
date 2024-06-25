from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.db_connector import create_db_and_tables
from app.routes import cart_routes, orders_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Order and Cart Service",
    description="API for managing orders",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Orders", "description": "Operations with orders."},
        {"name": "Carts", "description": "Operations with cart."}
    ]
)


@app.get("/")
def home():
    return "Welcome to Order Service"


app.include_router(router=orders_routes.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(router=cart_routes.router, prefix="/api/v1/cart", tags=["Carts"])
