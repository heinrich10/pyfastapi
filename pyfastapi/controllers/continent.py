from typing import List, Annotated
from sqlalchemy import ScalarResult
from fastapi import APIRouter, Depends, HTTPException, status, Path

from pyfastapi.models import Continent
from pyfastapi.repositories import ContinentRepository
from pyfastapi.schemas import ContinentSchema

router = APIRouter()


@router.get("/", response_model=List[ContinentSchema])
def get_all_continents(repo: Annotated[ContinentRepository, Depends()]) -> ScalarResult[Continent]:
    continents = repo.get_continents()
    return continents


@router.get("/{code}", response_model=ContinentSchema)
def get_one_continents(
    repo: Annotated[ContinentRepository, Depends()],
    code: Annotated[str, Path(title="continent code")]
) -> Continent:
    continent = repo.get_continent(code)
    if not continent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Continent {code} not found")
    return continent
