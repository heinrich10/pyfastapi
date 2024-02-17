
from .base import BaseRepository
from pyfastapi.models.continent import Continent


class ContinentRepository(BaseRepository):

    def get_continent(self, code: str):
        return self.db.query(Continent).filter(Continent.code == code).first()

    def get_continents(self):
        return self.db.query(Continent).all()
