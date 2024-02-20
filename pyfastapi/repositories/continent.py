from sqlalchemy import ScalarResult
from sqlalchemy.sql import select

from pyfastapi.models import Continent
from .base import BaseRepository


class ContinentRepository(BaseRepository):

    def get_continent(self, code: str) -> Continent | None:
        stmt = select(Continent).where(Continent.code == code)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_continents(self) -> ScalarResult[Continent]:
        return self.db.execute(select(Continent)).scalars()
