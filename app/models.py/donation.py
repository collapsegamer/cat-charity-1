from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import AbstractBase

REPR_TEMPLATE = '{base} comment={comment}'


class Donation(AbstractBase):
    comment: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self):
        base = super().__repr__()
        return REPR_TEMPLATE.format(base=base, comment=self.comment)
