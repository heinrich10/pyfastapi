from fastapi import FastAPI
from .controllers.person import router as person_router
from .controllers.country import router as country_router
from .controllers.continent import router as continent_router


app = FastAPI()

app.include_router(person_router, prefix="/persons")
app.include_router(country_router, prefix="/countries")
app.include_router(continent_router, prefix="/continents")


@app.get("/")
async def root():
    return {"message": "Hello World"}



