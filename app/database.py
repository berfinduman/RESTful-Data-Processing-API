# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database information is pulled from .env
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
