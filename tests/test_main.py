from fastapi.testclient import TestClient

from pyfastapi.main import app

client = TestClient(app)


def test_main_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
