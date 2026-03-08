from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class DonationCRUD(CRUDBase[Donation]):
    async def get_all(self, session: AsyncSession):
        result = await session.execute(
            select(Donation).order_by(Donation.create_date)
        )
        return result.scalars().all()


donation_crud = DonationCRUD(Donation)
