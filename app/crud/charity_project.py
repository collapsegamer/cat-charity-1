from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CharityProjectCRUD(CRUDBase[CharityProject]):
    async def get_all(self, session: AsyncSession):
        result = await session.execute(
            select(CharityProject).order_by(CharityProject.create_date)
        )
        return result.scalars().all()

    async def get_by_name(self, session: AsyncSession, name: str):
        result = await session.execute(
            select(CharityProject).where(CharityProject.name == name)
        )
        return result.scalars().first()


charity_project_crud = CharityProjectCRUD(CharityProject)
