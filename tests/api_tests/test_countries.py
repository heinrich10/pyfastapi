from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from pyfastapi.main import app
from pyfastapi.libs.db import get_db
from pyfastapi.models.country import Country
from tests.api_tests.util_pagination_helper import get_paginated

DEFAULT_LIMIT = 50
FIRST_COUNTRY = "AF"

client = TestClient(app)


def test_countries_seed_data():
    """
    if seed data is modified, this will fail
    """
    db: Session = next(get_db())
    count = db.query(Country.code).count()
    assert count == 252


def test_get_countries_default_limit():
    response, body = get_paginated("/countries", client)
    assert len(body['items']) == DEFAULT_LIMIT


def test_get_countries_limit_10():
    limit = "10"
    response, body = get_paginated("/countries", client, limit=limit)
    assert len(body["items"]) == int(limit)
    assert body["items"][0]["code"] == FIRST_COUNTRY


def test_get_countries_limit_5_offset_10():
    limit = "5"
    offset = "10"
    response, body = get_paginated("/countries", client, limit=limit, offset=offset)
    assert len(body["items"]) == int(limit)
    assert body["items"][0]["code"] != FIRST_COUNTRY


def test_get_one_country():
    country = "HK"
    response = client.get(f"/countries/{country}")
    body = response.json()
    assert response.status_code == 200
    assert body["code"] == country


def test_get_one_country_not_found():
    country = "ZZ"
    response = client.get(f"/countries/{country}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Country {country} not found"}
