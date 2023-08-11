
from pyfastapi.models.person import Person
from pyfastapi.schemas.person import PersonSchema
from sqlalchemy.orm import Session, joinedload


def get_person(db: Session, id_: int):
    return db.query(Person).options(joinedload(Person.country)).filter(Person.id == id_).first()


def get_persons(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Person).options(joinedload(Person.country)).offset(skip).limit(limit).all()


def create_person(db: Session, person: PersonSchema):
    pass
