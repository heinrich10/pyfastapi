
from ..models.country import Country
from sqlalchemy.orm import Session, contains_eager
from fastapi_pagination.ext.sqlalchemy import paginate


def get_country(db: Session, code: str):
    return db.query(Country).options(contains_eager(Country.continent)).filter(Country.code == code).first()


def get_countries(db: Session):
    return paginate(db.query(Country))
