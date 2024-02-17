from abc import ABC
from fastapi import Depends
from sqlalchemy.orm import Session

from pyfastapi.libs import get_db


class BaseRepository(ABC):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
