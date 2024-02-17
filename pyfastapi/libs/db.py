from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from pyfastapi.config import config


SQLALCHEMY_DATABASE_URL = config.get("DB_HOST")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
