from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker
from models import Base
import os

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]

# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://user:pass@network:port/dbname"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

# Define a SQLAlchemy model
session = SessionLocal()
Base.metadata.create_all(engine)