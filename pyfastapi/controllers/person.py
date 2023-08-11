
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from pyfastapi.repositories.person import get_person, get_persons
from pyfastapi.libs.db import get_db


router = APIRouter()


@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    person = get_persons(db)
    return person


@router.get("/{id_}")
def get_one_user(db: Session = Depends(get_db), id_: int = None):
    person = get_person(db, id_)
    return person
