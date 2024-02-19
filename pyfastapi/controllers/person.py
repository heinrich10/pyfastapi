import traceback
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi_pagination import LimitOffsetPage

from pyfastapi.models import Person
from pyfastapi.repositories import PersonRepository
from pyfastapi.schemas import PersonListSchema, PersonCreateSchema


router = APIRouter()


@router.get("/", response_model=LimitOffsetPage[PersonListSchema])
def get_all_persons(repo: Annotated[PersonRepository, Depends()]):
    person = repo.get_persons()
    return person


@router.get("/{id_}")
def get_one_persons(repo: Annotated[PersonRepository, Depends()], id_: int = None):
    person = repo.get_person(id_)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Person {id_} not found")
    return person


@router.post("/", response_model=PersonListSchema)
def create_person(body: PersonCreateSchema, repo: Annotated[PersonRepository, Depends()]):
    try:
        person = Person(
            first_name=body.first_name,
            last_name=body.last_name,
            country_code=body.country_code
        )
        new_person = repo.create_new_person(person)
        return new_person
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_}")
def update_person(id_: str, body: PersonCreateSchema, repo: Annotated[PersonRepository, Depends()]):
    person = Person(
        first_name=body.first_name,
        last_name=body.last_name,
        country_code=body.country_code
    )
    person.id = int(id_)
    repo.update_or_create_person(person)
    return Response(status_code=204)
