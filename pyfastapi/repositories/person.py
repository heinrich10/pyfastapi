from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import select

from pyfastapi.models.country import Country
from pyfastapi.models.person import Person
from .base import BaseRepository


class PersonRepository(BaseRepository):
    def get_person(self, id_: int) -> Person | None:
        return (self.db.execute(select(Person)
                .options(joinedload(Person.country).joinedload(Country.continent))
                .where(Person.id == id_)).scalar_one_or_none())

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
