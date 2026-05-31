from typing import Annotated
from fastapi import Depends
from sqlalchemy import ScalarResult

from pyfastapi.models import Continent
from pyfastapi.repositories import ContinentRepository
from pyfastapi.libs.exceptions import ContinentNotFoundError


class ContinentService:
    def __init__(self, repo: Annotated[ContinentRepository, Depends()]):
        self.repo = repo

    def get_continents(self) -> ScalarResult[Continent]:
        return self.repo.get_continents()

    def get_continent(self, code: str) -> Continent:
        continent = self.repo.get_continent(code)
        if not continent:
            raise ContinentNotFoundError(code)
        return continent
