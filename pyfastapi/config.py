from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    DB_HOST: str = "sqlite:///./sql_app.db"
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    LOG_LEVEL: str = "debug"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_config(file=".env") -> Settings:
    return Settings(_env_file=file)


__all__ = ["get_config"]
