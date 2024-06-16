from fastapi import FastAPI

from app.db.db_connector import create_db_and_tables

async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return "Welcome to User service"

# app.include_router(router=user_router)
# app.include_router(router=admin_route)