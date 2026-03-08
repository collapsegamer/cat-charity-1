from typing import Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, session: AsyncSession, obj_id: int):
        return await session.get(self.model, obj_id)

    async def create(self, session: AsyncSession, obj: ModelType):
        session.add(obj)
        return obj

    async def delete(self, session: AsyncSession, obj: ModelType):
        await session.delete(obj)
        return obj
