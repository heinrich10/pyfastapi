"""
End-to-end API tests that exercise full request/response flows
across multiple endpoints and entities.
"""

from fastapi.testclient import TestClient
from fastapi_pagination import LimitOffsetPage
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from pyfastapi.models import Person, Country, Continent
from pyfastapi.schemas import PersonListSchema, PersonSchema, CountryListSchema, ContinentSchema


def test_person_full_crud_flow(init_db: None, client: TestClient, db_session: Session) -> None:
    """
    Create a person, retrieve them by ID, list with filter, update, and verify.
    """
    # 1. Create
    create_data = {
        "first_name": "End",
        "last_name": "ToEnd",
        "country_code": "PH",
    }
    create_response = client.post("/persons", json=create_data)
    assert create_response.status_code == 200
    created: PersonListSchema = PersonListSchema(**create_response.json())
    assert created.first_name == "End"
    assert created.last_name == "ToEnd"
    assert created.country_code == "PH"
    assert created.id is not None
    person_id = created.id

    # Verify the person was actually persisted in the database
    person_from_db: Person = db_session.execute(
        select(Person).where(Person.id == person_id)
    ).scalar_one()
    assert person_from_db.first_name == "End"
    assert person_from_db.last_name == "ToEnd"
    assert person_from_db.country_code == "PH"

    # 2. Get by ID
    get_response = client.get(f"/persons/{person_id}")
    assert get_response.status_code == 200
    fetched: PersonSchema = PersonSchema(**get_response.json())
    assert fetched.id == person_id
    assert fetched.first_name == "End"
    assert fetched.country.code == "PH"
    assert fetched.country.continent.code is not None

    # 3. List with filter
    list_response = client.get("/persons?first_name=End&last_name=ToEnd")
    assert list_response.status_code == 200
    page = LimitOffsetPage(**list_response.json())
    assert page.total is not None and page.total >= 1
    assert any(p["id"] == person_id for p in page.items)

    # 4. Update
    update_data = {
        "first_name": "Updated",
        "last_name": "Name",
        "country_code": "HK",
    }
    put_response = client.put(f"/persons/{person_id}", json=update_data)
    assert put_response.status_code == 204

    # 5. Verify update in DB
    db_session.expire_all()
    stmt = select(Person).where(Person.id == person_id)
    updated_person: Person = db_session.execute(stmt).scalar_one()
    assert updated_person.first_name == "Updated"
    assert updated_person.last_name == "Name"
    assert updated_person.country_code == "HK"


def test_create_person_invalid_country_code_succeeds_on_sqlite(
    init_db: None, client: TestClient, db_session: Session
) -> None:
    """
    SQLite does not enforce foreign keys by default, so a non-existent country_code
    is accepted without error. This documents current behavior; a real database
    with FK enforcement would return an integrity error.
    """
    data = {
        "first_name": "Ghost",
        "last_name": "Rider",
        "country_code": "XX",
    }
    response = client.post("/persons", json=data)
    # SQLite default: no FK enforcement.
    assert response.status_code == 200
    created = PersonListSchema(**response.json())

    # Verify the row was actually inserted into the database
    person_from_db: Person = db_session.execute(
        select(Person).where(Person.id == created.id)
    ).scalar_one()
    assert person_from_db.first_name == "Ghost"
    assert person_from_db.country_code == "XX"


def test_get_person_not_found(init_db: None, client: TestClient) -> None:
    response = client.get("/persons/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Person 99999 not found"


def test_update_person_nonexistent_id_still_returns_204(init_db: None, client: TestClient, db_session: Session) -> None:
    """
    merge() semantics mean updating a non-existent ID may INSERT instead of 404.
    Document current behavior so regressions are visible.
    """
    data = {
        "first_name": "New",
        "last_name": "Person",
        "country_code": "PH",
    }
    response = client.put("/persons/99999", json=data)
    # Current implementation returns 204 regardless because merge() can create.
    assert response.status_code == 204

    # Verify merge() actually created the row in the database
    person_from_db: Person = db_session.execute(
        select(Person).where(Person.id == 99999)
    ).scalar_one()
    assert person_from_db.first_name == "New"
    assert person_from_db.country_code == "PH"


def test_countries_list_then_detail_flow(init_db: None, client: TestClient, db_session: Session) -> None:
    """
    List countries, pick the first one, then fetch its detail and verify nested continent.
    """
    list_response = client.get("/countries?limit=1")
    assert list_response.status_code == 200
    page = LimitOffsetPage(**list_response.json())
    assert page.items
    first = page.items[0]
    code = first["code"]

    detail_response = client.get(f"/countries/{code}")
    assert detail_response.status_code == 200
    detail: CountryListSchema = CountryListSchema(**detail_response.json())
    assert detail.code == code
    assert detail.continent_code is not None

    # Verify the country in the database matches the API response
    country_from_db: Country = db_session.execute(
        select(Country).where(Country.code == code)
    ).scalar_one()
    assert country_from_db.name == detail.name


def test_countries_filter_and_sort_flow(init_db: None, client: TestClient) -> None:
    """
    Filter countries by name and sort by name descending.
    """
    response = client.get("/countries?name=United&sort=-name")
    assert response.status_code == 200
    page = LimitOffsetPage(**response.json())
    assert page.total is not None and page.total >= 2
    names = [c["name"] for c in page.items]
    assert names == sorted(names, reverse=True)


def test_countries_pagination_boundary(init_db: None, client: TestClient) -> None:
    """
    Request an offset beyond the total count and verify empty items.
    """
    response = client.get("/countries?limit=10&offset=1000")
    assert response.status_code == 200
    page: LimitOffsetPage[CountryListSchema] = LimitOffsetPage(**response.json())
    assert page.items == []


def test_continents_list_then_detail_flow(init_db: None, client: TestClient) -> None:
    """
    List all continents and verify each one can be fetched by code.
    """
    list_response = client.get("/continents")
    assert list_response.status_code == 200
    continents: list[ContinentSchema] = [ContinentSchema(**c) for c in list_response.json()]
    assert len(continents) == 7

    for continent in continents:
        detail_response = client.get(f"/continents/{continent.code}")
        assert detail_response.status_code == 200
        detail = ContinentSchema(**detail_response.json())
        assert detail.code == continent.code
        assert detail.name == continent.name


def test_continent_not_found(init_db: None, client: TestClient, db_session: Session) -> None:
    response = client.get("/continents/XX")
    assert response.status_code == 404
    assert response.json()["detail"] == "Continent XX not found"

    # Verify the continent does not exist in the database
    continent_from_db = db_session.execute(
        select(Continent).where(Continent.code == "XX")
    ).scalar_one_or_none()
    assert continent_from_db is None


def test_persons_sort_then_filter_combination(init_db: None, client: TestClient) -> None:
    """
    Combine sort and filter parameters on the persons list endpoint.
    """
    response = client.get("/persons?country_code=US&sort=first_name")
    assert response.status_code == 200
    page = LimitOffsetPage(**response.json())
    assert page.total is not None and page.total >= 2
    for item in page.items:
        assert item["country_code"] == "US"


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
