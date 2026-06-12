from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage

from pyfastapi.libs.db import get_db
from pyfastapi.models import Person
from pyfastapi.repositories import PersonRepository, CountryRepository
from pyfastapi.schemas import PersonCreateSchema, QueryPersonSchema
from pyfastapi.libs.exceptions import PersonNotFoundError, CountryNotFoundError


class PersonService:
    def __init__(
        self,
        person_repo: Annotated[PersonRepository, Depends()],
        country_repo: Annotated[CountryRepository, Depends()],
        db: Annotated[Session, Depends(get_db)]
    ):
        self.person_repo = person_repo
        self.country_repo = country_repo
        self.db = db

    def get_persons(self, q: QueryPersonSchema, sort: str) -> LimitOffsetPage[Person]:
        return self.person_repo.get_persons(q, sort)

    def get_person(self, id_: int) -> Person:
        person = self.person_repo.get_person(id_)
        if not person:
            raise PersonNotFoundError(id_)
        return person

    def create_person(self, body: PersonCreateSchema) -> Person:
        if not self.country_repo.get_country(body.country_code):
            raise CountryNotFoundError(body.country_code)

        person = Person(
            first_name=body.first_name,
            last_name=body.last_name,
            country_code=body.country_code
        )
        new_person = self.person_repo.create_new_person(person)
        self.db.commit()
        self.db.refresh(new_person)
        return new_person

    def update_or_create_person(self, id_: int, body: PersonCreateSchema) -> None:
        if not self.country_repo.get_country(body.country_code):
            raise CountryNotFoundError(body.country_code)

        person = Person(
            first_name=body.first_name,
            last_name=body.last_name,
            country_code=body.country_code
        )
        person.id = id_
        self.person_repo.update_or_create_person(person)
        self.db.commit()

    def delete_person(self, id_: int) -> None:
        person = self.person_repo.get_person(id_)
        if not person:
            raise PersonNotFoundError(id_)

        self.person_repo.delete_person(person)
        self.db.commit()
