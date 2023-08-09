
from pydantic import BaseModel


class ContinentSchema(BaseModel):
    code: str
    name: str

    class Config:
        from_attributes = True
