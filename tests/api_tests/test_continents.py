from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from pyfastapi.main import app
from pyfastapi.libs.db import get_db
from pyfastapi.models.continent import Continent


client = TestClient(app)


def test_countries_seed_data():
    """
    if seed data is modified, this will fail
    """
    db: Session = next(get_db())
    count = db.query(Continent.code).count()
    assert count == 7


def test_get_continents():
    response = client.get("/continents")
    body = response.json()
    assert response.status_code == 200
    assert len(body) == 7


def test_get_one_continent():
    continent = "AF"
    response = client.get(f"/continents/{continent}")
    body = response.json()
    assert response.status_code == 200
    assert body["code"] == continent


def test_get_one_continent_not_found():
    continent = "ZZ"
    response = client.get(f"/continents/{continent}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Continent {continent} not found"}
