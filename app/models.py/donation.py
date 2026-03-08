from sqlalchemy import Column, Integer, Text

from app.models.base import InvestedBase


class Donation(InvestedBase):
    __tablename__ = "donation"

    id = Column(Integer, primary_key=True)
    comment = Column(Text, nullable=True)
