from typing import Sequence

from faker import Faker
from fastapi.testclient import TestClient
from fastapi_pagination import LimitOffsetPage
from pytest import fixture
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from pyfastapi.libs.db import get_db
from pyfastapi.main import app
from pyfastapi.models import Person
from pyfastapi.schemas import PersonListSchema
from pyfastapi.schemas.person import PersonSchema
from tests.api_tests.util_pagination_helper import get_paginated

DEFAULT_LIMIT = 50
FIRST_PERSON = 1

client = TestClient(app)


@fixture(scope="function")
def add_50_records(faker: Faker) -> None:
    db: Session = next(get_db())
    person_list = []
    for i in range(50):
        name = faker.name().split()
        person = Person(
            first_name=name[1],
            last_name=name[0],
            country_code="HK"
        )
        person_list.append(person)
    db.bulk_save_objects(person_list)
    db.commit()


def test_persons_seed_data() -> None:
    """
    if seed data is modified, this will fail
    """
    db: Session = next(get_db())
    count = db.query(Person.id).count()
    assert count == 13


def test_persons_default_pagination(add_50_records: None) -> None:
    body: LimitOffsetPage[Person]
    response, body = get_paginated("/persons", client)
    items: Sequence[Person] = body.items
    body_length = len(items)
    assert body_length == DEFAULT_LIMIT


def test_persons_limit_10() -> None:
    limit = "10"
    body: LimitOffsetPage[PersonListSchema]
    response, body = get_paginated("/persons", client, limit=limit)
    assert len(body.items) == int(limit)
    person: PersonListSchema = PersonListSchema.model_validate(body.items[0])
    assert person.id == FIRST_PERSON


def test_persons_limit_5_offset_10(add_50_records: None) -> None:
    limit = "5"
    offset = "10"
    body: LimitOffsetPage[PersonListSchema]
    response, body = get_paginated("/persons", client, limit=limit, offset=offset)
    assert len(body.items) == int(limit)
    person: PersonListSchema = PersonListSchema.model_validate(body.items[0])
    assert person.id != FIRST_PERSON


def test_get_one_person() -> None:
    person_id = 1
    response = client.get(f"/persons/{person_id}")
    print("test_get_one_person", response.json())
    body: PersonSchema = PersonSchema(**response.json())
    country = body.country
    continent = country.continent
    assert response.status_code == 200
    assert body.id == person_id
    assert all(hasattr(country, k) for k in ["code", "name", "phone", "symbol", "capital", "currency", "alpha_3"])
    assert all(hasattr(continent, k) for k in ["code", "name"])


def test_get_one_person_not_found() -> None:
    person_id = 0
    response = client.get(f"/persons/{person_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Person {person_id} not found"}


def test_create_person() -> None:
    first_name = "test1"
    last_name = "test2"
    country_code = "PH"
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "country_code": country_code,
    }
    response = client.post("/persons/", json=data)
    body: PersonListSchema = PersonListSchema(**response.json())
    assert body.first_name == first_name
    assert body.last_name == last_name
    assert body.country_code == country_code
    assert body.id is not None

    # should add 1 to total
    db: Session = next(get_db())
    count: int = db.query(Person.id).count()
    assert count == 14


def test_update_person() -> None:
    first_name = "test1"
    last_name = "test2"
    country_code = "PH"
    id_ = "1"
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "country_code": country_code
    }
    response1 = client.get(f"/persons/{id_}")
    body1 = response1.json()
    assert body1["first_name"] != first_name
    assert body1["last_name"] != last_name
    # TODO also check for country
    # assert body1["country_code"] != country_code
    response2 = client.put(f"/persons/{id_}", json=data)
    assert response2.status_code == 204

    db: Session = next(get_db())
    body2: Person = db.execute(select(Person).where(Person.id == id_)).scalar_one()
    assert body2.first_name == first_name
    assert body2.last_name == last_name
    assert body2.country_code == country_code
