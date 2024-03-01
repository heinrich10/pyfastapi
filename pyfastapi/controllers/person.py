import traceback
from typing import Annotated
from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, Response, status, Path
from fastapi_pagination import LimitOffsetPage

from pyfastapi.models import Person
from pyfastapi.repositories import PersonRepository
from pyfastapi.schemas import PersonListSchema, PersonCreateSchema, PersonSchema, QueryPersonSchema

router = APIRouter()
logger = getLogger(__name__)


@router.get("/", response_model=LimitOffsetPage[PersonListSchema])
def get_all_persons(
        q: Annotated[QueryPersonSchema, Depends()],
        repo: Annotated[PersonRepository, Depends()]
) -> LimitOffsetPage[Person]:
    person = repo.get_persons(q)
    return person


@router.get("/{id_}", response_model=PersonSchema)
def get_one_persons(
    repo: Annotated[PersonRepository, Depends()],
    id_: Annotated[int, Path(title="person id")]
) -> Person:
    person = repo.get_person(id_)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Person {id_} not found")
    return person


@router.post("/", response_model=PersonListSchema)
def create_person(body: PersonCreateSchema, repo: Annotated[PersonRepository, Depends()]) -> Person:
    logger.debug(f"body {body}")
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
def update_person(
    id_: Annotated[int, Path(title="person id")],
    body: PersonCreateSchema,
    repo: Annotated[PersonRepository, Depends()]
) -> Response:
    logger.debug(f"body {body}")
    person = Person(
        first_name=body.first_name,
        last_name=body.last_name,
        country_code=body.country_code
    )
    person.id = int(id_)
    repo.update_or_create_person(person)
    return Response(status_code=204)
