from typing import List, Iterator

from alembic import command
from alembic.config import Config
from pytest import fixture

from pyfastapi.utils.config import get_config

pytest_plugins = ["faker"]
AppConfig = get_config()


@fixture(autouse=True)
def init_db() -> Iterator[None]:
    """
    this is equivalent to "alembic upgrade head" then run "alembic downgrade base" after 1 test is done
    runs every test to make sure we have a clean set of data
    """
    config = Config()
    config.set_main_option("sqlalchemy.url", AppConfig.DB_HOST)
    config.set_main_option("script_location", "alembic")
    command.upgrade(config, "head")
    yield None
    command.downgrade(config, "base")


# faker fixtures below
@fixture(scope="session", autouse=True)
def faker_session_locale() -> List[str]:
    return ["en_US"]


@fixture(scope="session", autouse=True)
def faker_seed() -> int:
    return 12345
