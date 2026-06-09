from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import select

from pyfastapi.models import Person
from pyfastapi.schemas import QueryPersonSchema, SortPersonEnum
from .base import BaseRepository, extract_sort, extract_query


class PersonRepository(BaseRepository):
    def get_person(self, id_: int) -> Person | None:
        stmt = select(Person).options(joinedload(Person.country)).where(Person.id == id_)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_persons(self, q: QueryPersonSchema, sort: str) -> LimitOffsetPage[Person]:
        stmt = select(Person)
        stmt = extract_sort(Person, SortPersonEnum, sort, stmt)
        stmt = extract_query(Person, ["first_name", "last_name"], q, stmt)
        person_list: LimitOffsetPage[Person] = paginate(self.db, stmt)
        return person_list

    def create_new_person(self, person: Person) -> Person:
        self.db.add(person)
        self.db.flush()
        return person

    def update_or_create_person(self, person: Person) -> None:
        stmt = insert(Person).values(
            id=person.id,
            first_name=person.first_name,
            last_name=person.last_name,
            country_code=person.country_code
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[Person.id],
            set_={
                "first_name": stmt.excluded.first_name,
                "last_name": stmt.excluded.last_name,
                "country_code": stmt.excluded.country_code,
            }
        )
        self.db.execute(stmt)
