from pydantic import BaseModel


class ContinentSchema(BaseModel):
    code: str
    name: str

    model_config = {
        "from_attributes": True
    }
