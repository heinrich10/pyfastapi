import os
from functools import lru_cache
from logging import getLogger

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = getLogger(__name__)


class Settings(BaseSettings):
    def __init__(self, _env_file: str) -> None:
        super().__init__(_env_file=_env_file)

    DB_HOST: str = "sqlite:///./sql_app.db"
    HOST: str = "0.0.0.0"
    PORT: int = 3000
    LOG_LEVEL: str = "info"
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict()


@lru_cache
def get_config() -> Settings:
    """
    Get the configuration settings.
    Uses the ENVIRONMENT env var to decide which env file to load.
    """
    env_file = ".env.test" if os.getenv("ENVIRONMENT") == "test" else ".env"
    logger.info(f"loading env file {env_file}")
    return Settings(_env_file=env_file)


__all__ = ["get_config"]
