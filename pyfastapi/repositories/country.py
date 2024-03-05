from toolz.functoolz import compose  # type: ignore
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import select

from pyfastapi.models import Country
from pyfastapi.schemas import QueryCountrySchema, SortCountryEnum
from .base import BaseRepository, extract_sort, extract_query


class CountryRepository(BaseRepository):
    def get_country(self, code: str) -> Country | None:
        stmt = select(Country).options(joinedload(Country.continent)).where(Country.code == code)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_countries(self, q: QueryCountrySchema, sort: str) -> LimitOffsetPage[Country]:
        f = compose(
            extract_query(Country, ["name"], q),
            extract_sort(Country, SortCountryEnum, sort)
        )
        stmt = f(select(Country))
        country_list: LimitOffsetPage[Country] = paginate(self.db, stmt)
        return country_list
