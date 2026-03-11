from sqlalchemy import Column, String, Text

from app.models.base import InvestmentBase
from app.constants.constants import NAME_MAX_LEN


class CharityProject(InvestmentBase):
    __tablename__ = "charityproject"

    name = Column(String(NAME_MAX_LEN), unique=True, nullable=False)
    description = Column(Text, nullable=False)
