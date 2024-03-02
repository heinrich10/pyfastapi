from typing import Tuple
from toolz.functoolz import compose, curry  # type: ignore
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import Select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import select

from pyfastapi.models import Country
from pyfastapi.schemas import QueryCountrySchema, SortCountryEnum
from .base import BaseRepository


@curry  # type: ignore
def extract_query(
    q: QueryCountrySchema, stmt: Select[Tuple[Country]]
) -> Select[Tuple[Country]]:
    stmt_ = stmt
    for attr, value in q:
        if value is not None:
            if attr == "name":
                stmt_ = stmt_.where(getattr(Country, attr).ilike(f"%{value}%"))
            else:
                stmt_ = stmt_.where(getattr(Country, attr) == value)
    return stmt_


@curry  # type: ignore
def extract_sort(sort: str, stmt: Select[Tuple[Country]]) -> Select[Tuple[Country]]:
    stmt_ = stmt
    sort_key = sort[1:]
    if sort_key in SortCountryEnum:
        if sort[0] == "-":
            stmt_ = stmt_.order_by(getattr(Country, sort_key).desc())
        else:
            stmt_ = stmt_.order_by(getattr(Country, sort_key).asc())
    return stmt_


class CountryRepository(BaseRepository):
    def get_country(self, code: str) -> Country | None:
        stmt = select(Country).options(joinedload(Country.continent)).where(Country.code == code)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_countries(self, q: QueryCountrySchema, sort: str) -> LimitOffsetPage[Country]:
        f = compose(extract_query(q), extract_sort(sort))
        stmt = f(select(Country))
        country_list: LimitOffsetPage[Country] = paginate(self.db, stmt)
        return country_list
