from fastapi.testclient import TestClient


def get_paginated(path: str, client: TestClient, **kwargs):
    params = {"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
    params = {k: v for k, v in params.items() if v}
    response = client.get(
        url=path,
        params=params
    )
    body = response.json()
    assert response.status_code == 200
    assert all(k in body for k in ["items", "total", "limit", "offset"])
    return response, body
