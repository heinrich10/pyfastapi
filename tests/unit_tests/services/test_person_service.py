from unittest.mock import MagicMock
import pytest
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage

from pyfastapi.services.person import PersonService
from pyfastapi.repositories import PersonRepository, CountryRepository
from pyfastapi.schemas import PersonCreateSchema, QueryPersonSchema
from pyfastapi.models import Person, Country
from pyfastapi.libs.exceptions import PersonNotFoundError, CountryNotFoundError


@pytest.fixture
def mock_person_repo() -> MagicMock:
    return MagicMock(spec=PersonRepository)


@pytest.fixture
def mock_country_repo() -> MagicMock:
    return MagicMock(spec=CountryRepository)


@pytest.fixture
def mock_db() -> MagicMock:
    return MagicMock(spec=Session)


@pytest.fixture
def person_service(mock_person_repo: MagicMock, mock_country_repo: MagicMock, mock_db: MagicMock) -> PersonService:
    return PersonService(mock_person_repo, mock_country_repo, mock_db)


class TestPersonService:
    def test_get_persons(self, person_service: PersonService, mock_person_repo: MagicMock) -> None:
        q = QueryPersonSchema()
        sort = "name"
        mock_person_repo.get_persons.return_value = MagicMock(spec=LimitOffsetPage)

        result = person_service.get_persons(q, sort)

        mock_person_repo.get_persons.assert_called_once_with(q, sort)
        assert result == mock_person_repo.get_persons.return_value

    def test_get_person_success(self, person_service: PersonService, mock_person_repo: MagicMock) -> None:
        person_id = 1
        expected_person = Person(id=person_id, first_name="John", last_name="Doe")
        mock_person_repo.get_person.return_value = expected_person

        result = person_service.get_person(person_id)

        mock_person_repo.get_person.assert_called_once_with(person_id)
        assert result == expected_person

    def test_get_person_not_found(self, person_service: PersonService, mock_person_repo: MagicMock) -> None:
        person_id = 999
        mock_person_repo.get_person.return_value = None

        with pytest.raises(PersonNotFoundError) as exc:
            person_service.get_person(person_id)

        assert exc.value.status_code == 404
        assert str(person_id) in exc.value.message

    def test_create_person_success(
        self, person_service: PersonService, mock_person_repo: MagicMock, mock_country_repo: MagicMock, mock_db: MagicMock
    ) -> None:
        body = PersonCreateSchema(first_name="Jane", last_name="Doe", country_code="US")
        mock_country_repo.get_country.return_value = MagicMock(spec=Country)

        created_person = Person(id=1, first_name="Jane", last_name="Doe", country_code="US")
        mock_person_repo.create_new_person.return_value = created_person

        result = person_service.create_person(body)

        mock_country_repo.get_country.assert_called_once_with("US")
        mock_person_repo.create_new_person.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(created_person)
        assert result == created_person

    def test_create_person_country_not_found(self, person_service: PersonService, mock_country_repo: MagicMock) -> None:
        body = PersonCreateSchema(first_name="Jane", last_name="Doe", country_code="XX")
        mock_country_repo.get_country.return_value = None

        with pytest.raises(CountryNotFoundError):
            person_service.create_person(body)

        mock_country_repo.get_country.assert_called_once_with("XX")

    def test_update_person_success(
        self, person_service: PersonService, mock_person_repo: MagicMock, mock_country_repo: MagicMock, mock_db: MagicMock
    ) -> None:
        person_id = 1
        body = PersonCreateSchema(first_name="Jane", last_name="Doe", country_code="US")
        mock_country_repo.get_country.return_value = MagicMock(spec=Country)

        person_service.update_person(person_id, body)

        mock_country_repo.get_country.assert_called_once_with("US")
        mock_person_repo.update_or_create_person.assert_called_once()
        # Verify the person object passed to repo has correct ID
        args, _ = mock_person_repo.update_or_create_person.call_args
        passed_person = args[0]
        assert passed_person.id == person_id
        assert passed_person.first_name == "Jane"

        mock_db.commit.assert_called_once()

    def test_update_person_country_not_found(self, person_service: PersonService, mock_country_repo: MagicMock) -> None:
        person_id = 1
        body = PersonCreateSchema(first_name="Jane", last_name="Doe", country_code="XX")
        mock_country_repo.get_country.return_value = None

        with pytest.raises(CountryNotFoundError):
            person_service.update_person(person_id, body)

        mock_country_repo.get_country.assert_called_once_with("XX")
