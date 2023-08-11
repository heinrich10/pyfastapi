from os import environ
from dotenv import load_dotenv

load_dotenv()

config = {
    "DB_HOST": environ.get("DB_HOST"),
}
