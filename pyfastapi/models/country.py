from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, deferred, Mapped, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .person import Person
    from .continent import Continent


class Country(Base):
    __tablename__ = "countries"

    code: Mapped[str] = mapped_column(String(2), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[int] = mapped_column(Integer, nullable=False)
    symbol: Mapped[str] = mapped_column(String(10))
    capital: Mapped[str] = mapped_column(String(80))
    currency: Mapped[str] = mapped_column(String(3))
    continent_code: Mapped[str] = deferred(mapped_column(String(2), ForeignKey("continents.code")))
    alpha_3: Mapped[str] = mapped_column(String(3))

    person: Mapped["Person"] = relationship(back_populates="country")
    continent: Mapped["Continent"] = relationship(back_populates="country")

    def __repr__(self) -> str:
        return f"Country('{self.code}, {self.name}')"
