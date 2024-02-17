from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from pyfastapi.repositories import ContinentRepository
from pyfastapi.schemas import ContinentSchema

router = APIRouter()


@router.get("/", response_model=List[ContinentSchema])
def get_all_continents(repo: ContinentRepository = Depends(ContinentRepository)):
    continents = repo.get_continents()
    print("this is", continents)
    return continents


@router.get("/{code}", response_model=ContinentSchema)
def get_one_continents(repo: ContinentRepository = Depends(ContinentRepository), code: str = None):
    continent = repo.get_continent(code)
    if not continent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Continent {code} not found")
    return continent
