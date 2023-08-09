from fastapi import FastAPI
from fastapi_pagination import add_pagination

from .controllers.person import router as person_router
from .controllers.country import router as country_router
from .controllers.continent import router as continent_router

app = FastAPI()


app.include_router(person_router, prefix="/persons")
app.include_router(country_router, prefix="/countries")
app.include_router(continent_router, prefix="/continents")
app.add_api_route(
    "/health",
    endpoint=lambda : {"status": "ok"},
    methods=["GET"]
)


app = add_pagination(app)

