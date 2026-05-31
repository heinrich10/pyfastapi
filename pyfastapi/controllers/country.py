from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from fastapi_pagination import LimitOffsetPage

from pyfastapi.models import Country
from pyfastapi.schemas import CountryListSchema, QueryCountrySchema
from pyfastapi.services.country import CountryService

router = APIRouter()


@router.get("", response_model=LimitOffsetPage[CountryListSchema])
def get_all_countries(
        q: Annotated[QueryCountrySchema, Depends()],
        service: Annotated[CountryService, Depends()],
        sort: Annotated[str, Query(description="sort by")] = ""
) -> LimitOffsetPage[Country]:
    return service.get_countries(q, sort)


@router.get("/{code}", response_model=CountryListSchema)
def get_one_country(
    service: Annotated[CountryService, Depends()],
    code: Annotated[str, Path(title="country code")]
) -> Country:
    return service.get_country(code)
