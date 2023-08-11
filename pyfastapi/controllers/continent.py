from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from pyfastapi.repositories.continent import get_continent, get_continents
from pyfastapi.libs.db import get_db


router = APIRouter()


@router.get("/")
def get_all_continents(db: Session = Depends(get_db)):
    continents = get_continents(db)
    return continents


@router.get("/{code}")
def get_one_continents(db: Session = Depends(get_db), code: str = None):
    continent = get_continent(db, code)
    if not continent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Continent {code} not found")
    return continent
