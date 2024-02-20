from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from pyfastapi.controllers import person_router, country_router, continent_router

app = FastAPI()


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
