from fastapi_pagination import LimitOffsetPage
from sqlalchemy.orm import joinedload
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.sql import select

from .base import BaseRepository
from pyfastapi.models.country import Country


class CountryRepository(BaseRepository):

    def get_country(self, code: str) -> Country | None:
        return self.db.execute(
            select(Country).options(joinedload(Country.continent)).where(Country.code == code)
        ).scalar_one_or_none()

    def get_countries(self) -> LimitOffsetPage[Country]:
        country_list: LimitOffsetPage[Country] = paginate(self.db, select(Country))
        return country_list
