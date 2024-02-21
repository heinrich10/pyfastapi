from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, func

from pyfastapi.libs.db import get_db
from pyfastapi.main import app
from pyfastapi.models import Continent
from pyfastapi.schemas import ContinentSchema

client = TestClient(app)


def test_countries_seed_data() -> None:
    """
    if seed data is modified, this will fail
    """
    db: Session = next(get_db())
    stmt = select(func.count()).select_from(Continent)
    count = db.execute(stmt).scalar_one()
    assert count == 7


def test_get_continents() -> None:
    response = client.get("/continents")
    body = response.json()
    assert response.status_code == 200
    assert len(body) == 7


def test_get_one_continent() -> None:
    continent = "AF"
    response = client.get(f"/continents/{continent}")
    body: ContinentSchema = ContinentSchema(**response.json())
    assert response.status_code == 200
    assert body.code == continent


def test_get_one_continent_not_found() -> None:
    continent = "ZZ"
    response = client.get(f"/continents/{continent}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Continent {continent} not found"}
