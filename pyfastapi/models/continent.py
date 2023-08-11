from sqlalchemy import Column, String
from sqlalchemy.orm import Relationship

from pyfastapi.libs.db import Base


class Continent(Base):
    __tablename__ = "continents"

    code = Column(String(2), primary_key=True)
    name = Column(String(100), nullable=False)

    country = Relationship("Country", back_populates="continent")

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return f"Country('{self.code}, {self.name}')"



