from sqlalchemy.orm import joinedload
from fastapi_pagination.ext.sqlalchemy import paginate

from .base import BaseRepository
from pyfastapi.models.person import Person
from pyfastapi.models.country import Country


class PersonRepository(BaseRepository):
    def get_person(self, id_: int):
        return (self.db.query(Person)
                .options(joinedload(Person.country).joinedload(Country.continent))
                .filter(Person.id == id_).first())

    def get_persons(self):
        return paginate(self.db.query(Person))

    def create_new_person(self, person: Person):
        self.db.add(person)
        self.db.commit()
        self.db.refresh(person)
        return person

    def update_or_create_person(self, person: Person):
        self.db.merge(person)
        self.db.commit()
