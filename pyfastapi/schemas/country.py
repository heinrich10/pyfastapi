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

    model_config = {
        "from_attributes": True
    }


class CountrySchema(CountryBaseSchema):
    continent: ContinentSchema


class CountryListSchema(CountryBaseSchema):
    continent_code: str
