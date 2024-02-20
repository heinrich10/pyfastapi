from fastapi.testclient import TestClient
from fastapi_pagination import LimitOffsetPage
from sqlalchemy.orm import Session

from pyfastapi.main import app
from pyfastapi.libs.db import get_db
from pyfastapi.models import Country
from pyfastapi.schemas import CountryListSchema
from tests.api_tests.util_pagination_helper import get_paginated

DEFAULT_LIMIT = 50
FIRST_COUNTRY = "AF"

client = TestClient(app)


def test_countries_seed_data() -> None:
    """
    if seed data is modified, this will fail
    """
    db: Session = next(get_db())
    count = db.query(Country.code).count()
    assert count == 252


def test_get_countries_default_limit() -> None:
    body: LimitOffsetPage[CountryListSchema]
    response, body = get_paginated("/countries", client)
    assert len(body.items) == DEFAULT_LIMIT


def test_get_countries_limit_10() -> None:
    limit = "10"
    body: LimitOffsetPage[CountryListSchema]
    response, body = get_paginated("/countries", client, limit=limit)
    assert len(body.items) == int(limit)
    country = body.items[0]
    assert country.code == FIRST_COUNTRY


def test_get_countries_limit_5_offset_10() -> None:
    limit = "5"
    offset = "10"
    body: LimitOffsetPage[CountryListSchema]
    response, body = get_paginated("/countries", client, limit=limit, offset=offset)
    assert len(body.items) == int(limit)
    country = body.items[0]
    assert country.code != FIRST_COUNTRY


def test_get_one_country() -> None:
    country = "HK"
    response = client.get(f"/countries/{country}")
    body: CountryListSchema = CountryListSchema(**response.json())
    assert response.status_code == 200
    assert body.code == country


def test_get_one_country_not_found() -> None:
    country = "ZZ"
    response = client.get(f"/countries/{country}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Country {country} not found"}
