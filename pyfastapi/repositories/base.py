from abc import ABC
from typing import Annotated, Tuple, List, Type
from toolz.functoolz import curry  # type: ignore

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy.orm import Session

from pyfastapi.libs import get_db
from pyfastapi.models.base import Base
from pyfastapi.schemas.base import BaseEnum


class BaseRepository(ABC):
    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db


@curry  # type: ignore
def extract_query(
    model: Type[BaseModel], use_like_list: List[str], q: BaseModel, stmt: Select[Tuple[Base]]
) -> Select[Tuple[Base]]:
    """
    because of the @curry, return type is being ignored and is using Any
    """
    stmt_ = stmt
    for attr, value in q:
        if value is not None:
            if attr in use_like_list:
                stmt_ = stmt_.where(getattr(model, attr).ilike(f"%{value}%"))
            else:
                stmt_ = stmt_.where(getattr(model, attr) == value)
    return stmt_


@curry  # type: ignore
def extract_sort(
    model: Type[BaseModel], enum: Type[BaseEnum], sort: str, stmt: Select[Tuple[Type[Base]]]
) -> Select[Tuple[Type[Base]]]:
    """
    because of the @curry, return type is being ignored and is using Any
    """
    if sort:
        stmt_ = stmt
        first_char = sort[0]
        sort_key = sort[1:] if first_char in ["-", "+"] else sort

        if sort_key in enum:
            if sort[0] == "-":
                stmt_ = stmt_.order_by(getattr(model, sort_key).desc())
            else:
                stmt_ = stmt_.order_by(getattr(model, sort_key).asc())
        return stmt_
    else:
        return stmt
