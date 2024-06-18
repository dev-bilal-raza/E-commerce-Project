from typing import Annotated
from fastapi import Depends
from app.settings import DATABASE_URL
from sqlmodel import create_engine, Session, SQLModel

connection_str = str(DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg")

engine = create_engine(connection_str)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

DB_SESSION = Annotated[Session, Depends(get_session)]