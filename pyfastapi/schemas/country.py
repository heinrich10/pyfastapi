
from pydantic import BaseModel

from pyfastapi.schemas import ContinentSchema


class CountryBaseSchema(BaseModel):
    code: str
    name: str
    phone: int
    symbol: str
    capital: str
    currency: str
    alpha_3: str

    class Config:
        from_attributes = True


class CountrySchema(CountryBaseSchema):
    continents: ContinentSchema


class CountryListSchema(CountryBaseSchema):
    continent_code: str
