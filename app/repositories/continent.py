
from ..models.continent import Continent
from sqlalchemy.orm import Session


def get_continent(db: Session, code: str):
    return db.query(Continent).filter(Continent.code == code).first()


def get_continents(db: Session):
    return db.query(Continent).all()
