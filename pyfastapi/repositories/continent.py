from typing import List
from sqlalchemy import ScalarResult
from sqlalchemy.sql import select

from .base import BaseRepository
from pyfastapi.models.continent import Continent


class ContinentRepository(BaseRepository):

    def get_continent(self, code: str) -> Continent | None:
        return self.db.execute(select(Continent).where(Continent.code == code)).scalar_one_or_none()

    def get_continents(self) -> ScalarResult[Continent]:
        return self.db.execute(select(Continent)).scalars()
