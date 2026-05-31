from unittest.mock import MagicMock
import pytest
from fastapi_pagination import LimitOffsetPage

from pyfastapi.services.country import CountryService
from pyfastapi.repositories import CountryRepository
from pyfastapi.schemas import QueryCountrySchema
from pyfastapi.models import Country
from pyfastapi.libs.exceptions import CountryNotFoundError


@pytest.fixture
def mock_country_repo() -> MagicMock:
    return MagicMock(spec=CountryRepository)


@pytest.fixture
def country_service(mock_country_repo: MagicMock) -> CountryService:
    return CountryService(mock_country_repo)


class TestCountryService:
    def test_get_countries(self, country_service: CountryService, mock_country_repo: MagicMock) -> None:
        q = QueryCountrySchema()
        sort = "name"
        mock_country_repo.get_countries.return_value = MagicMock(spec=LimitOffsetPage)

        result = country_service.get_countries(q, sort)

        mock_country_repo.get_countries.assert_called_once_with(q, sort)
        assert result == mock_country_repo.get_countries.return_value

    def test_get_country_success(self, country_service: CountryService, mock_country_repo: MagicMock) -> None:
        code = "US"
        expected_country = Country(code=code, name="United States")
        mock_country_repo.get_country.return_value = expected_country

        result = country_service.get_country(code)

        mock_country_repo.get_country.assert_called_once_with(code)
        assert result == expected_country

    def test_get_country_not_found(self, country_service: CountryService, mock_country_repo: MagicMock) -> None:
        code = "XX"
        mock_country_repo.get_country.return_value = None

        with pytest.raises(CountryNotFoundError) as exc:
            country_service.get_country(code)

        assert exc.value.status_code == 404
        assert code in exc.value.message
