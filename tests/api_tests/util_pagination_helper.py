from typing import Tuple, TypeVar

from fastapi.testclient import TestClient
from fastapi_pagination import LimitOffsetPage
from httpx import Response

T = TypeVar("T")


def get_paginated(path: str, client: TestClient, **kwargs: str) -> Tuple[Response, LimitOffsetPage[T]]:
    params = {"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
    params = {k: v for k, v in params.items() if v}
    response: Response = client.get(
        url=path,
        params=params
    )
    body: LimitOffsetPage[T] = LimitOffsetPage(**response.json())
    assert response.status_code == 200
    assert all(hasattr(body, k) for k in ["items", "total", "limit", "offset"])
    return response, body
