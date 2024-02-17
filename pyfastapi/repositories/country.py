from sqlalchemy.orm import joinedload
from fastapi_pagination.ext.sqlalchemy import paginate

from .base import BaseRepository
from pyfastapi.models.country import Country


class CountryRepository(BaseRepository):

    def get_country(self, code: str):
        return self.db.query(Country).options(joinedload(Country.continent)).filter(Country.code == code).first()

    def get_countries(self):
        return paginate(self.db.query(Country))
