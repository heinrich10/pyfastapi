from pyfastapi.schemas.person import PersonSchema
from sqlalchemy.orm import Session, joinedload
from fastapi_pagination.ext.sqlalchemy import paginate

from pyfastapi.models.person import Person
from pyfastapi.models.country import Country


def get_person(db: Session, id_: int):
    return (db.query(Person)
            .options(joinedload(Person.country).joinedload(Country.continent))
            .filter(Person.id == id_).first())


def get_persons(db: Session):
    return paginate(db.query(Person))


def create_person(db: Session, person: PersonSchema):
    pass
