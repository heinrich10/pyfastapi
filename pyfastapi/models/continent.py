from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .country import Country


class Continent(Base):
    __tablename__ = "continents"

    code: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    country: Mapped["Country"] = relationship(back_populates="continent")

    def __repr__(self) -> str:
        return f"Continent('{self.code}, {self.name}')"
