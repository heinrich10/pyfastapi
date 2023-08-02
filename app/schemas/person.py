
from pydantic import BaseModel


class PersonSchema(BaseModel):
    id: int
    last_name: str
    first_name: str
    country_code: str

    class Config:
        from_attributes = True
