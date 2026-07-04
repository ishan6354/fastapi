from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 
# Think of Base as a blueprint factory: every time you make a class that inherits from Base, 
# SQLAlchemy records that class as a table definition. 
# That registry is what SQLAlchemy uses to build SQL, create tables, and map rows to Python objects.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# 1. create a new Session for this request
# 2. yield hand the Session to FastAPI and to the caller          
# 3. always close the Session after the request