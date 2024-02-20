from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi_pagination import LimitOffsetPage

from pyfastapi.models import Country
from pyfastapi.repositories import CountryRepository
from pyfastapi.schemas import CountryListSchema

router = APIRouter()


@router.get("/", response_model=LimitOffsetPage[CountryListSchema])
def get_all_countries(repo: Annotated[CountryRepository, Depends()]) -> LimitOffsetPage[Country]:
    country = repo.get_countries()
    return country


@router.get("/{code}", response_model=CountryListSchema)
def get_one_country(
    repo: Annotated[CountryRepository, Depends()],
    code: Annotated[str, Path(title="country code")]
) -> Country:
    country = repo.get_country(code)
    if not country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Country {code} not found")
    return country
