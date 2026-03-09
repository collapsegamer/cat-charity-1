from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt
from pydantic import ConfigDict


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class DonationDB(DonationCreate):
    id: int
    create_date: datetime
    close_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class DonationFullInfoDB(DonationDB):
    invested_amount: int
    fully_invested: bool
