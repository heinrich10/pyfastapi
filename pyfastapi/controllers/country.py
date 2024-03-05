from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from fastapi_pagination import LimitOffsetPage

from pyfastapi.models import Country
from pyfastapi.repositories import CountryRepository
from pyfastapi.schemas import CountryListSchema, QueryCountrySchema

router = APIRouter()


@router.get("/", response_model=LimitOffsetPage[CountryListSchema])
def get_all_countries(
        q: Annotated[QueryCountrySchema, Depends()],
        repo: Annotated[CountryRepository, Depends()],
        sort: Annotated[str, Query(description="sort by")] = ""
) -> LimitOffsetPage[Country]:
    country = repo.get_countries(q, sort)
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
