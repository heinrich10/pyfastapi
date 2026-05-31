from unittest.mock import MagicMock
import pytest
from sqlalchemy import ScalarResult

from pyfastapi.services.continent import ContinentService
from pyfastapi.repositories import ContinentRepository
from pyfastapi.models import Continent
from pyfastapi.libs.exceptions import ContinentNotFoundError


@pytest.fixture
def mock_continent_repo() -> MagicMock:
    return MagicMock(spec=ContinentRepository)


@pytest.fixture
def continent_service(mock_continent_repo: MagicMock) -> ContinentService:
    return ContinentService(mock_continent_repo)


class TestContinentService:
    def test_get_continents(self, continent_service: ContinentService, mock_continent_repo: MagicMock) -> None:
        mock_continent_repo.get_continents.return_value = MagicMock(spec=ScalarResult)

        result = continent_service.get_continents()

        mock_continent_repo.get_continents.assert_called_once()
        assert result == mock_continent_repo.get_continents.return_value

    def test_get_continent_success(self, continent_service: ContinentService, mock_continent_repo: MagicMock) -> None:
        code = "AS"
        expected_continent = Continent(code=code, name="Asia")
        mock_continent_repo.get_continent.return_value = expected_continent

        result = continent_service.get_continent(code)

        mock_continent_repo.get_continent.assert_called_once_with(code)
        assert result == expected_continent

    def test_get_continent_not_found(self, continent_service: ContinentService, mock_continent_repo: MagicMock) -> None:
        code = "XX"
        mock_continent_repo.get_continent.return_value = None

        with pytest.raises(ContinentNotFoundError) as exc:
            continent_service.get_continent(code)

        assert exc.value.status_code == 404
        assert code in exc.value.message
