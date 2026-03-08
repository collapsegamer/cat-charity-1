from datetime import datetime

from pydantic import BaseModel, PositiveInt, constr


class CharityProjectCreate(BaseModel):
    name: constr(min_length=5, max_length=100)
    description: constr(min_length=10)
    full_amount: PositiveInt

    class Config:
        extra = "forbid"


class CharityProjectUpdate(BaseModel):
    name: constr(min_length=5, max_length=100) | None = None
    description: constr(min_length=10) | None = None
    full_amount: PositiveInt | None = None

    class Config:
        extra = "forbid"


class CharityProjectDB(BaseModel):
    id: int
    name: str
    description: str
    full_amount: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime | None = None

    class Config:
        from_attributes = True
