
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import LimitOffsetPage
from sqlalchemy.orm import Session

from pyfastapi.repositories.person import get_person, get_persons
from pyfastapi.libs.db import get_db
from pyfastapi.schemas.person import PersonListSchema


router = APIRouter()


@router.get("/", response_model=LimitOffsetPage[PersonListSchema])
def get_all_users(db: Session = Depends(get_db)):
    person = get_persons(db)
    return person


@router.get("/{id_}")
def get_one_user(db: Session = Depends(get_db), id_: int = None):
    person = get_person(db, id_)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Person {id_} not found")
    return person
