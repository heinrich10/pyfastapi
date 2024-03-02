from typing import Tuple

from sqlalchemy import Select
from toolz .functoolz import compose, curry  # type: ignore
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.sql import select

from pyfastapi.models import Person, Country
from .base import BaseRepository
from pyfastapi.schemas import QueryPersonSchema, SortPersonEnum


@curry  # type: ignore
def extract_query(
    q: QueryPersonSchema, stmt: Select[Tuple[Person]]
) -> Select[Tuple[Person]]:
    stmt_ = stmt
    for attr, value in q:
        if value is not None:
            if attr == "first_name" or attr == "last_name":
                stmt_ = stmt_.where(getattr(Person, attr).ilike(f"%{value}%"))
            else:
                stmt_ = stmt_.where(getattr(Person, attr) == value)
    return stmt_


@curry  # type: ignore
def extract_sort(sort: str, stmt: Select[Tuple[Person]]) -> Select[Tuple[Person]]:
    stmt_ = stmt
    sort_key = sort[1:]
    if sort_key in SortPersonEnum:
        if sort[0] == "-":
            stmt_ = stmt_.order_by(getattr(Person, sort_key).desc())
        else:
            stmt_ = stmt_.order_by(getattr(Person, sort_key).asc())
    return stmt_


class PersonRepository(BaseRepository):
    def get_person(self, id_: int) -> Person | None:
        stmt = select(Person, Country).join(Country, Person.country_code == Country.code).where(Person.id == id_)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_persons(self, q: QueryPersonSchema, sort: str) -> LimitOffsetPage[Person]:
        f = compose(extract_query(q), extract_sort(sort))
        stmt = f(select(Person))
        person_list: LimitOffsetPage[Person] = paginate(self.db, stmt)
        return person_list

    def create_new_person(self, person: Person) -> Person:
        self.db.add(person)
        self.db.commit()
        self.db.refresh(person)
        return person

    def update_or_create_person(self, person: Person) -> None:
        self.db.merge(person)
        self.db.commit()
