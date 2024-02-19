from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_HOST = environ.get("DB_HOST", "sqlite:///./sql_app.db")
    HOST = environ.get("HOST", "0.0.0.0")
    PORT = int(environ.get("PORT", "5000"))
    LOG_LEVEL = environ.get("LOG_LEVEL", "debug")
