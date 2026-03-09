from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import AbstractBase

REPR_TEMPLATE = '{base} name={name} description={description}'


class CharityProject(AbstractBase):
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self):
        base = super().__repr__()
        return REPR_TEMPLATE.format(
            base=base,
            name=self.name,
            description=self.description
        )
