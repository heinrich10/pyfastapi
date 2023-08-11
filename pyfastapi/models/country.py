from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Relationship, deferred
from pyfastapi.libs.db import Base


class Country(Base):
    __tablename__ = "countries"

    code = Column(String(2), primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(Integer, nullable=False)
    symbol = Column(String(10))
    capital = Column(String(80))
    currency = Column(String(3))
    continent_code = deferred(Column(String(2), ForeignKey("continents.code")))
    alpha_3 = Column(String(3))

    person = Relationship("Person", back_populates="country")
    continent = Relationship("Continent", back_populates="country")

    def __init__(self, code, name, phone, symbol, capital, currency, continent_code, alpha_3):
        self.code = code
        self.name = name
        self.phone = phone
        self.symbol = symbol
        self.capital = capital
        self.currency = currency
        self.continent_code = continent_code
        self.alpha_3 = alpha_3

    def __repr__(self):
        return f"Country('{self.code}, {self.name}')"



