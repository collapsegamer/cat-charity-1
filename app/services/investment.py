from datetime import datetime
from typing import Sequence, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation

ModelType = Union[CharityProject, Donation]


def _close_instance(instance: ModelType) -> None:
    instance.fully_invested = True
    instance.close_date = datetime.now()


def _invest(
    targets: Sequence[ModelType],
    source: ModelType,
) -> None:
    if source.invested_amount is None:
        source.invested_amount = 0

    for target in targets:
        if target.invested_amount is None:
            target.invested_amount = 0

        if source.fully_invested:
            break

        source_remainder = source.full_amount - source.invested_amount
        target_remainder = target.full_amount - target.invested_amount

        if source_remainder <= 0:
            _close_instance(source)
            break

        if target_remainder <= 0:
            _close_instance(target)
            continue

        amount = min(source_remainder, target_remainder)
        source.invested_amount += amount
        target.invested_amount += amount

        if target.invested_amount == target.full_amount:
            _close_instance(target)

        if source.invested_amount == source.full_amount:
            _close_instance(source)
            break


async def invest_new_donation(
    donation: Donation,
    session: AsyncSession,
) -> Donation:
    open_projects = await charity_project_crud.get_open_objects(session)
    _invest(open_projects, donation)
    return await donation_crud.commit_investment(
        session=session,
        source=donation,
        targets=open_projects,
    )


async def invest_new_project(
    project: CharityProject,
    session: AsyncSession,
) -> CharityProject:
    open_donations = await donation_crud.get_open_objects(session)
    _invest(open_donations, project)
    return await charity_project_crud.commit_investment(
        session=session,
        source=project,
        targets=open_donations,
    )
