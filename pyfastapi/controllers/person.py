from typing import Annotated
from logging import getLogger

from fastapi import APIRouter, Depends, Response, Path, Query
from fastapi_pagination import LimitOffsetPage

from pyfastapi.models import Person
from pyfastapi.schemas import PersonListSchema, PersonCreateSchema, PersonSchema, QueryPersonSchema
from pyfastapi.services.person import PersonService

router = APIRouter()
logger = getLogger(__name__)


@router.get("", response_model=LimitOffsetPage[PersonListSchema])
def get_all_persons(
        service: Annotated[PersonService, Depends()],
        q: Annotated[QueryPersonSchema, Depends()],
        sort: Annotated[str, Query(description="sort by")] = ""
) -> LimitOffsetPage[Person]:
    return service.get_persons(q, sort)


@router.get("/{id_}", response_model=PersonSchema)
def get_one_person(
    service: Annotated[PersonService, Depends()],
    id_: Annotated[int, Path(title="person id")]
) -> Person:
    return service.get_person(id_)


@router.post("", response_model=PersonListSchema)
def create_person(body: PersonCreateSchema, service: Annotated[PersonService, Depends()]) -> Person:
    logger.debug(f"body {body}")
    return service.create_person(body)


@router.put("/{id_}")
def update_person(
    id_: Annotated[int, Path(title="person id")],
    body: PersonCreateSchema,
    service: Annotated[PersonService, Depends()]
) -> Response:
    logger.debug(f"body {body}")
    service.update_person(int(id_), body)
    return Response(status_code=204)
