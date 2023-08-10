
from pytest import fixture
from alembic.config import Config
from alembic import command

from app.config import config as app_config


@fixture(scope='session')
def init_db():
    config = Config()
    config.set_main_option("sqlalchemy.url", app_config["DB_HOST"])
    config.set_main_option("script_location", "alembic")
    command.upgrade(config, 'head')
    yield None
    command.downgrade(config, 'base')

