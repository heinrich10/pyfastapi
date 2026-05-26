from typing import Sequence

from faker import Faker
from fastapi.testclient import TestClient
from fastapi_pagination import LimitOffsetPage
from pytest import fixture
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, func

from pyfastapi.models import Person
from pyfastapi.schemas import PersonListSchema, PersonSchema, CountrySchema
from tests.api_tests.util_pagination_helper import get_paginated

DEFAULT_LIMIT = 50
FIRST_PERSON = 1
NUM_SEED_DATA = 13


@fixture(scope="function")
def add_50_records(faker: Faker, db_session: Session) -> None:
    person_list = []
    for i in range(50):
        name = faker.name().split()
        person = Person(
            first_name=name[1],
            last_name=name[0],
            country_code="HK"
        )
        person_list.append(person)
    db_session.bulk_save_objects(person_list)
    db_session.commit()


@fixture(scope="function")
def add_juan_dela_cruz(db_session: Session) -> None:
    person = Person(
        first_name="Juan",
        last_name="dela Cruz",
        country_code="PH"
    )
    db_session.add(person)
    db_session.commit()


def test_persons_seed_data(init_db: None, db_session: Session) -> None:
    """
    if seed data is modified, this will fail
    """
    stmt = select(func.count()).select_from(Person)
    count = db_session.execute(stmt).scalar_one()
    assert count == NUM_SEED_DATA


def test_persons_default_pagination(init_db: None, add_50_records: None, client: TestClient) -> None:
    body: LimitOffsetPage[Person]
    response, body = get_paginated("/persons", client)
    items: Sequence[Person] = body.items
    body_length = len(items)
    assert body_length == DEFAULT_LIMIT


def test_persons_limit_10(init_db: None, client: TestClient) -> None:
    limit = "10"
    body: LimitOffsetPage[PersonListSchema]
    response, body = get_paginated("/persons", client, limit=limit)
    assert len(body.items) == int(limit)
    person: PersonListSchema = PersonListSchema.model_validate(body.items[0])
    assert person.id == FIRST_PERSON


def test_persons_limit_5_offset_10(init_db: None, add_50_records: None, client: TestClient) -> None:
    limit = "5"
    offset = "10"
    body: LimitOffsetPage[PersonListSchema]
    response, body = get_paginated("/persons", client, limit=limit, offset=offset)
    assert len(body.items) == int(limit)
    person: PersonListSchema = PersonListSchema.model_validate(body.items[0])
    assert person.id != FIRST_PERSON


def test_persons_with_filter(init_db: None, add_juan_dela_cruz: None, client: TestClient) -> None:
    filter_ = "first_name=juan&last_name=cruz"
    body: LimitOffsetPage[PersonListSchema]
    response, body = get_paginated(f"/persons?{filter_}", client)
    assert len(body.items) == 1
    person: PersonListSchema = PersonListSchema.model_validate(body.items[0])
    assert person.last_name == "dela Cruz"
    assert person.first_name == "Juan"
    assert person.country_code == "PH"


def test_persons_with_sort_asc(init_db: None, client: TestClient) -> None:
    sort = "first_name"
    body: LimitOffsetPage[PersonListSchema]
    response, body = get_paginated(f"/persons?sort={sort}", client)
    assert len(body.items) == NUM_SEED_DATA
    person: PersonListSchema = PersonListSchema.model_validate(body.items[0])
    assert person.first_name == "Adam"


def test_persons_with_sort_desc(init_db: None, client: TestClient) -> None:
    sort = "-first_name"
    body: LimitOffsetPage[PersonListSchema]
    response, body = get_paginated(f"/persons?sort={sort}", client)
    assert len(body.items) == NUM_SEED_DATA
    person: PersonListSchema = PersonListSchema.model_validate(body.items[0])
    assert person.first_name == "Zoe"


def test_get_one_person(init_db: None, client: TestClient, db_session: Session) -> None:
    person_id = 1
    response = client.get(f"/persons/{person_id}")
    body: PersonSchema = PersonSchema(**response.json())
    country = body.country
    continent = country.continent
    assert response.status_code == 200
    assert body.id == person_id
    assert all(hasattr(country, k) for k in ["code", "name", "phone", "symbol", "capital", "currency", "alpha_3"])
    assert all(hasattr(continent, k) for k in ["code", "name"])

    # Verify the same data is present in the database
    person_from_db: Person = db_session.execute(
        select(Person).where(Person.id == person_id)
    ).scalar_one()
    assert person_from_db.first_name == body.first_name
    assert person_from_db.last_name == body.last_name


def test_get_one_person_not_found(init_db: None, client: TestClient, db_session: Session) -> None:
    person_id = 0
    response = client.get(f"/persons/{person_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Person {person_id} not found"}

    # Verify the person does not exist in the database
    person_from_db = db_session.execute(
        select(Person).where(Person.id == person_id)
    ).scalar_one_or_none()
    assert person_from_db is None


def test_create_person(init_db: None, client: TestClient, db_session: Session) -> None:
    first_name = "test1"
    last_name = "test2"
    country_code = "PH"
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "country_code": country_code,
    }
    response = client.post("/persons", json=data)
    body: PersonListSchema = PersonListSchema(**response.json())
    assert body.first_name == first_name
    assert body.last_name == last_name
    assert body.country_code == country_code
    assert body.id is not None

    # Verify the specific record was persisted in the database
    person_from_db: Person = db_session.execute(
        select(Person).where(Person.id == body.id)
    ).scalar_one()
    assert person_from_db.first_name == first_name
    assert person_from_db.last_name == last_name
    assert person_from_db.country_code == country_code

    # Verify total count increased by 1
    count: int = db_session.execute(select(func.count()).select_from(Person)).scalar_one()
    assert count == NUM_SEED_DATA + 1


def test_update_person(init_db: None, client: TestClient, db_session: Session) -> None:
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
    current_person: PersonSchema = PersonSchema(**response1.json())
    assert current_person.first_name != first_name
    assert current_person.last_name != last_name
    current_country: CountrySchema = current_person.country
    assert current_country.code != country_code

    response2 = client.put(f"/persons/{id_}", json=data)
    assert response2.status_code == 204

    stmt = select(Person).where(Person.id == id_)
    updated_person: Person = db_session.execute(stmt).scalar_one()
    assert updated_person.first_name == first_name
    assert updated_person.last_name == last_name
    assert updated_person.country_code == country_code
