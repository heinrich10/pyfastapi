
from pyfastapi.models.country import Country
from sqlalchemy.orm import Session, joinedload
from fastapi_pagination.ext.sqlalchemy import paginate


def get_country(db: Session, code: str):
    return db.query(Country).options(joinedload(Country.continent)).filter(Country.code == code).first()


def get_countries(db: Session):
    return paginate(db.query(Country))
