from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.sql import select

from pyfastapi.models import Person, Country
from .base import BaseRepository


class PersonRepository(BaseRepository):
    def get_person(self, id_: int) -> Person | None:
        stmt = select(Person, Country).join(Country, Person.country_code == Country.code).where(Person.id == id_)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_persons(self) -> LimitOffsetPage[Person]:
        person_list: LimitOffsetPage[Person] = paginate(self.db, select(Person))
        return person_list

    def create_new_person(self, person: Person) -> Person:
        self.db.add(person)
        self.db.commit()
        self.db.refresh(person)
        return person

    def update_or_create_person(self, person: Person) -> None:
        self.db.merge(person)
        self.db.commit()
