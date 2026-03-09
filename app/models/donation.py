from sqlalchemy import Column, Text

from app.models.base import InvestmentBase


class Donation(InvestmentBase):
    __tablename__ = "donation"

    comment = Column(Text, nullable=True)
