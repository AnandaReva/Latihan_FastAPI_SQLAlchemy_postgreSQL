# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:qwerqwer@localhost/cobafastapi" 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def connect_to_db():
    Base.metadata.create_all(bind=engine)

def disconnect_from_db():
    engine.dispose()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
