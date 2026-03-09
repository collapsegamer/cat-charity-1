"""Схемы данных для работы с целевыми проектами."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt
from pydantic import ConfigDict

from app.constants.constants import (
    DESC_MIN_LEN,
    NAME_MAX_LEN,
    NAME_MIN_LEN,
)


class CharityProjectCreate(BaseModel):
    """Схема создания целевого проекта."""

    name: str = Field(
        ...,
        min_length=NAME_MIN_LEN,
        max_length=NAME_MAX_LEN,
    )
    description: str = Field(
        ...,
        min_length=DESC_MIN_LEN,
    )
    full_amount: PositiveInt

    model_config = ConfigDict(extra="forbid")


class CharityProjectUpdate(BaseModel):
    """Схема обновления целевого проекта."""

    name: Optional[str] = Field(
        None,
        min_length=NAME_MIN_LEN,
        max_length=NAME_MAX_LEN,
    )
    description: Optional[str] = Field(
        None,
        min_length=DESC_MIN_LEN,
    )
    full_amount: Optional[PositiveInt] = None

    model_config = ConfigDict(extra="forbid")


class CharityProjectDB(CharityProjectCreate):
    """Схема данных проекта, возвращаемого из БД."""

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
