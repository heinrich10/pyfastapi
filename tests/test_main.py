from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_main_health(init_db):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
