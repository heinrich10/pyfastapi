import os
from typing import Iterator

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm import Session

from pyfastapi.libs.db import get_session_factory
from pyfastapi.main import app
from pyfastapi.utils.config import get_config

os.environ.setdefault("ENVIRONMENT", "test")

pytest_plugins = ["faker"]


@fixture(scope="function")
def init_db() -> Iterator[None]:
    """
    this is equivalent to "alembic upgrade head" then run "alembic downgrade base" after 1 test is done
    runs every test to make sure we have a clean set of data
    """
    app_config = get_config()
    config = Config()
    config.set_main_option("sqlalchemy.url", app_config.DB_HOST)
    config.set_main_option("script_location", "alembic")
    command.upgrade(config, "head")
    yield None
    command.downgrade(config, "base")


@fixture(scope="session")
def client() -> Iterator[TestClient]:
    with TestClient(app) as c:
        yield c


@fixture(scope="function")
def db_session() -> Iterator[Session]:
    factory = get_session_factory()
    db = factory()
    try:
        yield db
    finally:
        db.close()


# faker fixtures below
@fixture(scope="session", autouse=True)
def faker_session_locale() -> list[str]:
    return ["en_US"]


@fixture(scope="session", autouse=True)
def faker_seed() -> int:
    return 12345
