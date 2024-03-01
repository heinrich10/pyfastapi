from pydantic import BaseModel, Field

from pyfastapi.schemas import CountrySchema


class PersonBaseSchema(BaseModel):
    last_name: str = Field(default=None)
    first_name: str

    model_config = {
        "from_attributes": True
    }


class PersonSchema(PersonBaseSchema):
    id: int
    country: CountrySchema


class PersonListSchema(PersonBaseSchema):
    id: int
    country_code: str


class PersonCreateSchema(PersonBaseSchema):
    country_code: str


class QueryPersonSchema(BaseModel):
    last_name: str | None = None
    first_name: str | None = None
    country_code: str | None = None

