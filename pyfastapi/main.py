from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from pyfastapi.controllers import person_router, country_router, continent_router
from pyfastapi.libs.db import get_engine
from pyfastapi.libs.exceptions import DomainError
from pyfastapi.utils.logging import init_logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_logger()
    yield
    get_engine().dispose()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


app.include_router(person_router, prefix="/persons")
app.include_router(country_router, prefix="/countries")
app.include_router(continent_router, prefix="/continents")
app.add_api_route(
    "/health",
    endpoint=health,
    methods=["GET"]
)


app = add_pagination(app)
