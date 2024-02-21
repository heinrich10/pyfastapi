import sys
from functools import lru_cache
from logging import getLogger

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = getLogger(__name__)


class Settings(BaseSettings):

    def __init__(self, _env_file: str) -> None:
        super().__init__(_env_file=_env_file)

    DB_HOST: str = "sqlite:///./sql_app.db"
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    LOG_LEVEL: str = "info"

    model_config = SettingsConfigDict()


@lru_cache
def get_config() -> Settings:
    """
    Get the configuration settings
    This will check if it is running on pytest.
    If it is, it will use the .env.test file, otherwise it will use the .env file
    """
    file = ".env.test" if "pytest" in sys.modules else ".env"
    logger.info(f"logger input file {file}")
    return Settings(_env_file=file)


__all__ = ["get_config"]
