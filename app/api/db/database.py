import sqlalchemy
import databases
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..settings.config import settings as s


DATABASE_URL = f"postgresql://{s.POSTGRES_USER}:{s.POSTGRES_PASSWORD}@{s.POSTGRES_SERVER}/{s.POSTGRES_DB}"

database = databases.Database(DATABASE_URL)

metadata = MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
