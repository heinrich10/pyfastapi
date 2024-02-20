from typing import Tuple, Dict, Any, TypeVar, Iterable, cast

from fastapi_pagination import LimitOffsetPage
# from fastapi import Response
from httpx import Response
from fastapi.testclient import TestClient

T = TypeVar("T")


def get_paginated(path: str, client: TestClient, **kwargs: str) -> Tuple[Response, LimitOffsetPage[T]]:
    params = {"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
    params = {k: v for k, v in params.items() if v}
    response: Response = client.get(
        url=path,
        params=params
    )
    body: LimitOffsetPage[T] = response.json()
    # print("this is body", body)
    assert response.status_code == 200
    for k in ["items", "total", "limit", "offset"]:
        assert body[k] is not None
    # assert all(k in body for k in cast(Iterable[str], ["items", "total", "limit", "offset"]))
    return response, body
