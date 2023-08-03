
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..repositories.country import get_countries, get_country
from ..libs.db import get_db


router = APIRouter()


@router.get("/")
def get_all_countries(db: Session = Depends(get_db)):
    person = get_countries(db)
    return person


@router.get("/{code}")
def get_one_country(db: Session = Depends(get_db), code: str = None):
    person = get_country(db, code)
    return person
