
from pydantic import BaseModel

from pyfastapi.schemas.country import CountrySchema


class PersonBaseSchema(BaseModel):
    id: int
    last_name: str
    first_name: str

    class Config:
        from_attributes = True


class PersonSchema(PersonBaseSchema):
    country: CountrySchema


class PersonListSchema(PersonBaseSchema):
    country_code: str
