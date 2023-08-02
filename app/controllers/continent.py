
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..repositories.continent import get_continent, get_continents
from ..lib.db import get_db


router = APIRouter()


@router.get("/")
def get_all_continents(db: Session = Depends(get_db)):
    person = get_continents(db)
    return person


@router.get("/{code}")
def get_one_continents(db: Session = Depends(get_db), code: str = None):
    person = get_continent(db, code)
    return person
