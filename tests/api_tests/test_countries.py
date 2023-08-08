from fastapi.testclient import TestClient

from app.main import app

DEFAULT_LIMIT = 50
FIRST_COUNTRY = "AF"

client = TestClient(app)


def _get_countries(**kwargs):
    params = {"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
    params = {k: v for k, v in params.items() if v}
    print(params)
    response = client.get(
        url="/countries",
        params=params
    )
    body = response.json()
    assert response.status_code == 200
    assert all(k in body for k in ["items", "total", "limit", "offset"])
    return response, body


def test_get_countries_default_limit():
    response, body = _get_countries()
    assert len(body['items']) == DEFAULT_LIMIT


def test_get_countries_limit_10():
    limit = "10"
    response, body = _get_countries(limit=limit)
    assert len(body["items"]) == int(limit)
    assert body["items"][0]["code"] == FIRST_COUNTRY


def test_get_countries_limit_10_offset_10():
    limit = "5"
    offset = "10"
    response, body = _get_countries(limit=limit, offset=offset)
    assert len(body["items"]) == int(limit)
    assert body["items"][0]["code"] != FIRST_COUNTRY


def test_get_one_country():
    country = "HK"
    response = client.get(f"/countries/{country}")
    body = response.json()
    assert response.status_code == 200
    assert body["code"] == country


def test_get_one_country_not_found():
    country = "ZZ"
    response = client.get(f"/countries/{country}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Country {country} not found"}