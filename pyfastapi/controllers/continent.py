from typing import List, Annotated

from fastapi import APIRouter, Depends, Path
from sqlalchemy import ScalarResult

from pyfastapi.models import Continent
from pyfastapi.schemas import ContinentSchema
from pyfastapi.services.continent import ContinentService

router = APIRouter()


@router.get("", response_model=List[ContinentSchema])
def get_all_continents(service: Annotated[ContinentService, Depends()]) -> ScalarResult[Continent]:
    return service.get_continents()


@router.get("/{code}", response_model=ContinentSchema)
def get_one_continents(
    service: Annotated[ContinentService, Depends()],
    code: Annotated[str, Path(title="continent code")]
) -> Continent:
    return service.get_continent(code)
