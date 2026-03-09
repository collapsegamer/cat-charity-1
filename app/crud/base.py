from typing import Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar('ModelType')


class CRUDBase:
    """Базовый класс для операций работы с БД."""

    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get_open_objects(
        self,
        session: AsyncSession,
    ) -> list[ModelType]:
        """
        Вернуть «открытые» объекты в порядке FIFO.

        Предполагается, что модель имеет поля fully_invested и create_date.
        """
        result = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        return result.scalars().all()

    async def commit_investment(
        self,
        session: AsyncSession,
        source: ModelType,
        targets: Sequence[ModelType],
        commit: bool = True,
    ) -> ModelType:
        """
        Сохранить изменения инвестиций в базе данных.

        Параметр commit позволяет управлять тем, делать ли здесь commit.
        """
        session.add_all([source, *targets])
        if commit:
            await session.commit()
        await session.refresh(source)
        return source
