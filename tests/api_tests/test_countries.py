from fastapi.testclient import TestClient
from fastapi_pagination import LimitOffsetPage
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, func

from pyfastapi.models import Country
from pyfastapi.schemas import CountryListSchema
from tests.api_tests.util_pagination_helper import get_paginated

DEFAULT_LIMIT = 50
FIRST_COUNTRY = "AF"


def test_countries_seed_data(init_db: None, db_session: Session) -> None:
    """
    if seed data is modified, this will fail
    """
    stmt = select(func.count()).select_from(Country)
    count = db_session.execute(stmt).scalar_one()
    assert count == 252


def test_get_countries_default_limit(init_db: None, client: TestClient) -> None:
    body: LimitOffsetPage[CountryListSchema]
    response, body = get_paginated("/countries", client)
    assert len(body.items) == DEFAULT_LIMIT


def test_get_countries_limit_10(init_db: None, client: TestClient) -> None:
    limit = "10"
    body: LimitOffsetPage[CountryListSchema]
    response, body = get_paginated("/countries", client, limit=limit)
    assert len(body.items) == int(limit)
    country: CountryListSchema = CountryListSchema.model_validate(body.items[0])
    assert country.code == FIRST_COUNTRY


def test_get_countries_limit_5_offset_10(init_db: None, client: TestClient) -> None:
    limit = "5"
    offset = "10"
    body: LimitOffsetPage[CountryListSchema]
    response, body = get_paginated("/countries", client, limit=limit, offset=offset)
    assert len(body.items) == int(limit)
    country: CountryListSchema = CountryListSchema.model_validate(body.items[0])
    assert country.code != FIRST_COUNTRY


def test_get_countries_with_filter(init_db: None, client: TestClient) -> None:
    filter_ = "name=Hong Kong"
    body: LimitOffsetPage[CountryListSchema]
    response, body = get_paginated(f"/countries?{filter_}", client)
    assert len(body.items) == 1
    country: CountryListSchema = CountryListSchema.model_validate(body.items[0])
    assert country.name == "Hong Kong"


def test_get_countries_with_sort_asc(init_db: None, client: TestClient) -> None:
    sort = "name"
    body: LimitOffsetPage[CountryListSchema]
    response, body = get_paginated(f"/countries?sort={sort}", client)
    assert len(body.items) == DEFAULT_LIMIT
    country: CountryListSchema = CountryListSchema.model_validate(body.items[0])
    assert country.name == "Afghanistan"


def test_get_countries_with_sort_desc(init_db: None, client: TestClient) -> None:
    sort = "-name"
    body: LimitOffsetPage[CountryListSchema]
    response, body = get_paginated(f"/countries?sort={sort}", client)
    assert len(body.items) == DEFAULT_LIMIT
    country: CountryListSchema = CountryListSchema.model_validate(body.items[0])
    assert country.name == "Zimbabwe"


def test_get_one_country(init_db: None, client: TestClient, db_session: Session) -> None:
    country = "HK"
    response = client.get(f"/countries/{country}")
    body: CountryListSchema = CountryListSchema(**response.json())
    assert response.status_code == 200
    assert body.code == country

    # Verify the same record exists in the database
    country_from_db: Country = db_session.execute(
        select(Country).where(Country.code == country)
    ).scalar_one()
    assert country_from_db.name == body.name
    assert country_from_db.continent_code == body.continent_code


def test_get_one_country_not_found(init_db: None, client: TestClient, db_session: Session) -> None:
    country = "ZZ"
    response = client.get(f"/countries/{country}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Country {country} not found"}

    # Verify the country does not exist in the database
    country_from_db = db_session.execute(
        select(Country).where(Country.code == country)
    ).scalar_one_or_none()
    assert country_from_db is None
