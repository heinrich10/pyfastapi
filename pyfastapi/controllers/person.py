import traceback

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi_pagination import LimitOffsetPage
from sqlalchemy.orm import Session

from pyfastapi.models.person import Person
from pyfastapi.repositories.person import get_person, get_persons, create_new_person, update_or_create_person
from pyfastapi.libs.db import get_db
from pyfastapi.schemas.person import PersonListSchema, PersonCreateSchema


router = APIRouter()


@router.get("/", response_model=LimitOffsetPage[PersonListSchema])
def get_all_persons(db: Session = Depends(get_db)):
    person = get_persons(db)
    return person


@router.get("/{id_}")
def get_one_persons(db: Session = Depends(get_db), id_: int = None):
    person = get_person(db, id_)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Person {id_} not found")
    return person


@router.post("/", response_model=PersonListSchema)
def create_person(body: PersonCreateSchema, db: Session = Depends(get_db)):
    print("this is the body", body)
    try:
        person = Person(
            first_name=body.first_name,
            last_name=body.last_name,
            country_code=body.country_code
        )
        new_person = create_new_person(db, person)
        return new_person
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_}")
def update_person(id_: str, body: PersonCreateSchema, db: Session = Depends(get_db)):
    person = Person(
        first_name=body.first_name,
        last_name=body.last_name,
        country_code=body.country_code
    )
    person.id = int(id_)
    print("updating", person)
    update_or_create_person(db, person)
    return Response(status_code=204)
