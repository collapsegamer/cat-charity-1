from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base

REPR_TEMPLATE = '{name} id={id} full={full} invest={invest} closed={closed}'


class AbstractBase(Base):

    __abstract__ = True

    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    close_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    def recalculate_state(self) -> None:
        if self.invested_amount >= self.full_amount:
            self.fully_invested = True
            self.close_date = datetime.now()

    def __repr__(self):
        return REPR_TEMPLATE.format(
            name=type(self),
            id=self.id,
            full=self.full_amount,
            invest=self.invested_amount,
            closed=self.fully_invested
        )
