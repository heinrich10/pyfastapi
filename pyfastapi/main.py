from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from pyfastapi.controllers import person_router, country_router, continent_router
from pyfastapi.libs.exceptions import DomainError


app = FastAPI()


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
