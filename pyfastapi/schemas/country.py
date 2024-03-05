from pydantic import BaseModel

from pyfastapi.schemas import ContinentSchema
from .base import BaseEnum


class CountryBaseSchema(BaseModel):
    code: str
    name: str
    phone: int
    symbol: str
    capital: str
    currency: str
    alpha_3: str

    model_config = {
        "from_attributes": True
    }


class CountrySchema(CountryBaseSchema):
    continent: ContinentSchema


class CountryListSchema(CountryBaseSchema):
    continent_code: str


class QueryCountrySchema(BaseModel):
    name: str | None = None
    phone: int | None = None
    symbol: str | None = None
    capital: str | None = None
    currency: str | None = None
    alpha_3: str | None = None
    continent_code: str | None = None


class SortCountryEnum(BaseEnum):
    code: str = "code"
    name: str = "name"
    phone: str = "phone"
    symbol: str = "symbol"
    capital: str = "capital"
    currency: str = "currency"
    alpha_3: str = "alpha_3"
    continent_code: str = "continent_code"
