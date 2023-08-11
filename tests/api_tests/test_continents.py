from fastapi.testclient import TestClient

from pyfastapi.main import app


client = TestClient(app)


def test_get_continents():
    response = client.get("/continents")
    body = response.json()
    assert response.status_code == 200
    assert len(body) == 7


def test_get_one_continent():
    continent = "AF"
    response = client.get(f"/continents/{continent}")
    body = response.json()
    assert response.status_code == 200
    assert body["code"] == continent


def test_get_one_continent_not_found():
    continent = "ZZ"
    response = client.get(f"/continents/{continent}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Continent {continent} not found"}