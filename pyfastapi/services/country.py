from typing import Annotated
from fastapi import Depends
from fastapi_pagination import LimitOffsetPage

from pyfastapi.models import Country
from pyfastapi.repositories import CountryRepository
from pyfastapi.schemas import QueryCountrySchema
from pyfastapi.libs.exceptions import CountryNotFoundError


class CountryService:
    def __init__(self, repo: Annotated[CountryRepository, Depends()]):
        self.repo = repo

    def get_countries(self, q: QueryCountrySchema, sort: str) -> LimitOffsetPage[Country]:
        return self.repo.get_countries(q, sort)

    def get_country(self, code: str) -> Country:
        country = self.repo.get_country(code)
        if not country:
            raise CountryNotFoundError(code)
        return country
