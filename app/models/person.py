from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, deferred

from ..lib.db import Base
import app.models.country

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    country_code = deferred(Column(String(2), ForeignKey("countries.code")))

    country = relationship("Country", back_populates="person")

    def __init__(self, last_name, first_name, country_code):
        self.last_name = last_name
        self.first_name = first_name
        self.country_code = country_code

    def __repr__(self):
        return f"Person('{self.id}, {self.first_name}, {self.last_name}')"



