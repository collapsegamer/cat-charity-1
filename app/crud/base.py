from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get_open(
            self,
            session: AsyncSession
    ):
        return (await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )).scalars().all()

    async def get(
            self,
            obj_id,
            session: AsyncSession
    ):
        return (await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )).scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        return (await session.execute(select(self.model))).scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession
    ):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.flush()
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession
    ):
        await session.delete(db_obj)
        return db_obj
