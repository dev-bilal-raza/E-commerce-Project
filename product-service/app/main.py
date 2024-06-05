from fastapi import FastAPI
from app.db.db_connector import create_db_and_tables
from app.routes.product_routes import router

async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return "Welcome to Product service"

app.include_router(router=router, prefix="api")