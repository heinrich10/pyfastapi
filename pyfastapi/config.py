import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):

    def __init__(self, _env_file: str) -> None:
        super().__init__(_env_file=_env_file)

    DB_HOST: str = "sqlite:///./sql_app.db"
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    LOG_LEVEL: str = "debug"

    model_config = SettingsConfigDict()


@lru_cache
def get_config() -> Settings:
    file = ".env.test" if "pytest" in sys.modules else ".env"
    print('input file', file)
    return Settings(_env_file=file)


__all__ = ["get_config"]
