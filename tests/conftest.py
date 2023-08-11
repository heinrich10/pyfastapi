from pytest import fixture
from alembic.config import Config
from alembic import command
from dotenv import load_dotenv, find_dotenv


def pytest_configure():
    load_dotenv(find_dotenv(".env.test"))


@fixture(autouse=True)
def init_db():
    """
    this is equivalent to "alembic upgrade head" then run "alembic downgrade base" after 1 test is done
    runs every test to make sure we have a clean set of data
    """
    from pyfastapi.config import config as app_config
    config = Config()
    config.set_main_option("sqlalchemy.url", app_config["DB_HOST"])
    config.set_main_option("script_location", "alembic")
    command.upgrade(config, 'head')
    yield None
    command.downgrade(config, 'base')
