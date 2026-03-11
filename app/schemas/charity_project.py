from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt
from pydantic import ConfigDict

from app.constants.constants import (
    DESC_MIN_LEN,
    NAME_MAX_LEN,
    NAME_MIN_LEN,
)


class CharityProjectBase(BaseModel):
    """Общие поля для Create и DB схем."""
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


class CharityProjectCreate(CharityProjectBase):
    model_config = ConfigDict(extra="forbid")


class CharityProjectUpdate(BaseModel):
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


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)