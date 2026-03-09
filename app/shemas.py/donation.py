from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationResponse(DonationBase):
    id: int
    create_date: datetime


class DonationDB(DonationBase):
    id: int
    invested_amount: int
    fully_invested: Optional[bool] = False
    create_date: datetime
    close_date: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
