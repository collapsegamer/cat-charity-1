from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt
from pydantic import ConfigDict


class DonationBase(BaseModel):
    """Общие поля для Create и DB схем."""
    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    model_config = ConfigDict(extra="forbid")


class DonationDB(DonationBase):
    id: int
    create_date: datetime
    close_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class DonationFullInfoDB(DonationDB):
    invested_amount: int
    fully_invested: bool
