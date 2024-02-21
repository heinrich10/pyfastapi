from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, deferred, mapped_column, Mapped

from .base import Base

if TYPE_CHECKING:
    from .country import Country


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    country_code: Mapped[str] = deferred(mapped_column(String(2), ForeignKey("countries.code")))

    country: Mapped["Country"] = relationship(back_populates="person")

    def __repr__(self) -> str:
        return f"Person('{self.id}, {self.first_name}, {self.last_name}')"
