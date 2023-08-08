
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import LimitOffsetPage
from sqlalchemy.orm import Session

from ..repositories.country import get_countries, get_country
from ..schemas.country import CountryListSchema
from ..libs.db import get_db

router = APIRouter()


@router.get("/", response_model=LimitOffsetPage[CountryListSchema])
def get_all_countries(db: Session = Depends(get_db)):
    country = get_countries(db)
    return country


@router.get("/{code}")
def get_one_country(db: Session = Depends(get_db), code: str = None):
    country = get_country(db, code)
    if not country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Country {code} not found")
    return country
