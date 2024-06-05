from app.settings import DATABASE_URL
from sqlmodel import create_engine, SQLModel, Session
from fastapi import Depends
from typing import Annotated

# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL
connection_string = str(DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

# recycle connections after 5 minutes
# to correspond with the compute scale down
engine = create_engine(
    connection_string, pool_pre_ping=True, echo=True, pool_recycle=300
)

def get_session():
    with Session(engine) as session:
        yield session

DB_SESSION = Annotated[Session, Depends(get_session)]

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
