import psycopg2
from environs import Env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


env = Env()
env.read_env()

DB_USER = env.str('DB_USER')
DB_USER_PASSWORD = env.str('DB_USER_PASSWORD')
DB_HOST = env.str('DB_HOST')
DB_NAME = env.str('DB_NAME')


DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_USER_PASSWORD}@db/{DB_NAME}'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()