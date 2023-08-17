from pytest import fixture
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from pyfastapi.main import app
from pyfastapi.libs.db import get_db
from pyfastapi.models.person import Person
from tests.api_tests.util_pagination_helper import get_paginated


DEFAULT_LIMIT = 50
FIRST_PERSON = 1

client = TestClient(app)


@fixture(scope="function")
def add_50_records(faker):
    print('add_50_records')
    db: Session = next(get_db())
    person_list = []
    for i in range(50):
        name = faker.name().split()
        person_list.append(Person(name[1], name[0], "HK"))
    db.bulk_save_objects(person_list)
    db.commit()


def test_persons_seed_data():
    """
    if seed data is modified, this will fail
    """
    db: Session = next(get_db())
    count = db.query(Person.id).count()
    assert count == 13


def test_persons_default_pagination(add_50_records):
    response, body = get_paginated("/persons", client)
    print(body)
    assert len(body["items"]) == DEFAULT_LIMIT


def test_persons_limit_10():
    limit = "10"
    response, body = get_paginated("/persons", client, limit=limit)
    assert len(body["items"]) == int(limit)
    assert body["items"][0]["id"] == FIRST_PERSON


def test_persons_limit_5_offset_10(add_50_records):
    limit = "5"
    offset = "10"
    response, body = get_paginated("/persons", client, limit=limit, offset=offset)
    assert len(body["items"]) == int(limit)
    assert body["items"][0]["id"] != FIRST_PERSON


def test_get_one_person():
    person_id = 1
    response = client.get(f"/persons/{person_id}")
    body = response.json()
    country = body["country"]
    continent = country["continent"]
    assert response.status_code == 200
    assert body["id"] == person_id
    assert all(k in country for k in ["code", "name", "phone", "symbol", "capital", "currency", "alpha_3"])
    assert all(k in continent for k in ["code", "name"])


def test_get_one_person_not_found():
    person_id = 0
    response = client.get(f"/persons/{person_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Person {person_id} not found"}
