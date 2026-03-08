from sqlalchemy import Column, Integer, String, Text

from app.models.base import InvestedBase


class CharityProject(InvestedBase):
    __tablename__ = "charityproject"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
