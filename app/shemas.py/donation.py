from datetime import datetime

from pydantic import BaseModel, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: str | None = None

    class Config:
        extra = "forbid"


# POST /donation/ — строго "короткий" ответ (без invested_amount/fully_invested)
# + exclude_none в эндпоинте, чтобы comment не приходил как null, если его не было
class DonationCreateResponse(BaseModel):
    id: int
    full_amount: int
    comment: str | None = None
    create_date: datetime
    close_date: datetime | None = None

    class Config:
        from_attributes = True


# GET /donation/ — полный ответ
class DonationFullInfoDB(BaseModel):
    id: int
    full_amount: int
    comment: str | None = None
    create_date: datetime
    invested_amount: int
    fully_invested: bool
    close_date: datetime | None = None

    class Config:
        from_attributes = True
