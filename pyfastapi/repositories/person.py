from sqlalchemy.orm import joinedload
from sqlalchemy.sql import select
from fastapi_pagination.ext.sqlalchemy import paginate

from .base import BaseRepository
from pyfastapi.models.person import Person
from pyfastapi.models.country import Country


class PersonRepository(BaseRepository):
    def get_person(self, id_: int):
        return (self.db.execute(select(Person)
                .options(joinedload(Person.country).joinedload(Country.continent))
                .where(Person.id == id_)).scalar_one_or_none())

    def get_persons(self):
        return paginate(self.db, select(Person))

    def create_new_person(self, person: Person):
        self.db.add(person)
        self.db.commit()
        self.db.refresh(person)
        return person

    def update_or_create_person(self, person: Person):
        self.db.merge(person)
        self.db.commit()
