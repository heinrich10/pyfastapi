from abc import ABC
from typing import Annotated, Tuple, List, Type, TypeVar

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy.orm import Session

from pyfastapi.libs import get_db
from pyfastapi.models.base import Base
from pyfastapi.schemas.base import BaseEnum

T = TypeVar("T", bound=Base)


class BaseRepository(ABC):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db


def extract_query(
    model: Type[T], use_like_list: List[str], q: BaseModel, stmt: Select[Tuple[T]]
) -> Select[Tuple[T]]:
    stmt_ = stmt
    for attr, value in q:
        if value is not None:
            if attr in use_like_list:
                stmt_ = stmt_.where(getattr(model, attr).ilike(f"%{value}%"))
            else:
                stmt_ = stmt_.where(getattr(model, attr) == value)
    return stmt_


def extract_sort(
    model: Type[T], enum: Type[BaseEnum], sort: str, stmt: Select[Tuple[T]]
) -> Select[Tuple[T]]:
    if not sort:
        return stmt

    first_char = sort[0]
    sort_key = sort[1:] if first_char in ["-", "+"] else sort

    if sort_key in enum:
        if sort[0] == "-":
            return stmt.order_by(getattr(model, sort_key).desc())
        else:
            return stmt.order_by(getattr(model, sort_key).asc())
    return stmt
