from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import LimitOffsetPage

from pyfastapi.repositories import CountryRepository
from pyfastapi.schemas import CountryListSchema

router = APIRouter()


@router.get("/", response_model=LimitOffsetPage[CountryListSchema])
def get_all_countries(repo: CountryRepository = Depends(CountryRepository)):
    country = repo.get_countries()
    return country


@router.get("/{code}")
def get_one_country(repo: CountryRepository = Depends(CountryRepository), code: str = None):
    country = repo.get_country(code)
    if not country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Country {code} not found")
    return country
