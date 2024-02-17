from fastapi import APIRouter, Depends, HTTPException, status

from pyfastapi.repositories import ContinentRepository

router = APIRouter()


@router.get("/")
def get_all_continents(repo: ContinentRepository = Depends(ContinentRepository)):
    continents = repo.get_continents()
    return continents


@router.get("/{code}")
def get_one_continents(repo: ContinentRepository = Depends(ContinentRepository), code: str = None):
    continent = repo.get_continent(code)
    if not continent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Continent {code} not found")
    return continent
