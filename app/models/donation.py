"""Модель пожертвования в фонд QRKot."""

from sqlalchemy import Column, Text

from app.models.base import InvestmentBase


class Donation(InvestmentBase):
    """Модель пожертвования."""

    __tablename__ = "donation"

    comment = Column(Text, nullable=True)
