"""
OverView:
This file sets up DB connection, and gives FASTAPI a smooth means of creating sessions
and auto closing them
This file performs the following
- Engine: The phone line to the database, for future communications
- SessionLocal: A factory function that manages each calll with the database.
- Base: The blueprint for creating tables, helps SQLAlchemy do tis thing properly.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
# from .con

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)  
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
