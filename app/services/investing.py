from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


def _close(obj):
    obj.fully_invested = True
    obj.close_date = datetime.utcnow()


async def invest(session: AsyncSession, target):
    if isinstance(target, Donation):
        sources = (
            await session.execute(
                select(CharityProject)
                .where(CharityProject.fully_invested.is_(False))
                .order_by(CharityProject.create_date)
            )
        ).scalars().all()
    else:
        sources = (
            await session.execute(
                select(Donation)
                .where(Donation.fully_invested.is_(False))
                .order_by(Donation.create_date)
            )
        ).scalars().all()

    for source in sources:
        if target.fully_invested:
            break

        need = target.full_amount - target.invested_amount
        free = source.full_amount - source.invested_amount
        delta = min(need, free)

        if delta <= 0:
            continue

        target.invested_amount += delta
        source.invested_amount += delta

        if source.invested_amount == source.full_amount:
            _close(source)

        if target.invested_amount == target.full_amount:
            _close(target)

        session.add(source)
        session.add(target)
