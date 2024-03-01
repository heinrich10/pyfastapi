from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import select

from pyfastapi.models import Country
from pyfastapi.schemas import QueryCountrySchema
from .base import BaseRepository


class CountryRepository(BaseRepository):

    def get_country(self, code: str) -> Country | None:
        stmt = select(Country).options(joinedload(Country.continent)).where(Country.code == code)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_countries(self, q: QueryCountrySchema) -> LimitOffsetPage[Country]:
        stmt = select(Country)
        for attr, value in q:
            if value is not None:
                if attr == "name":
                    stmt = stmt.where(getattr(Country, attr).ilike(f"%{value}%"))
                else:
                    stmt = stmt.where(getattr(Country, attr) == value)

        country_list: LimitOffsetPage[Country] = paginate(self.db, stmt)
        return country_list
