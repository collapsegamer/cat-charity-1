"""Маршруты для работы с целевыми проектами."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import CharityProject
from app.schemas import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import invest_new_project

router = APIRouter(
    prefix="/charity_project",
    tags=["charity_projects"],
)

ERR_NOT_FOUND = "Проект не найден."
ERR_EXISTS = "Проект с таким именем уже существует!"
ERR_CLOSED = "Закрытый проект нельзя редактировать!"
ERR_AMOUNT = (
    "Нелья установить значение full_amount меньше "
    "уже вложенной суммы."
)
ERR_DELETE = (
    "В проект были внесены средства, не подлежит удалению!"
)


async def get_project_or_404(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Получить проект или вызвать 404."""
    project = await session.get(CharityProject, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERR_NOT_FOUND,
        )
    return project


@router.get(
    "/",
    response_model=list[CharityProjectDB],
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),  # noqa: B008
):
    """Получить список всех проектов."""
    result = await session.execute(
        select(CharityProject).order_by(CharityProject.id)
    )
    return result.scalars().all()


@router.post(
    "/",
    response_model=CharityProjectDB,
)
async def create_project(
    project_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),  # noqa: B008
):
    """Создать новый проект."""
    existing = await session.execute(
        select(CharityProject).where(
            CharityProject.name == project_in.name
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERR_EXISTS,
        )

    project = CharityProject(**project_in.model_dump())
    session.add(project)
    await session.flush()
    await invest_new_project(project, session)

    await session.commit()
    await session.refresh(project)
    return project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
)
async def update_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),  # noqa: B008
):
    """Обновить данные проекта."""
    project = await get_project_or_404(project_id, session)

    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERR_CLOSED,
        )

    update_data = project_in.model_dump(exclude_unset=True)

    new_name = update_data.get("name")
    if new_name and new_name != project.name:
        existing = await session.execute(
            select(CharityProject).where(
                CharityProject.name == new_name
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERR_EXISTS,
            )

    new_amount = update_data.get("full_amount")
    if new_amount is not None and new_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERR_AMOUNT,
        )

    for field, value in update_data.items():
        setattr(project, field, value)

    if (
        project.invested_amount >= project.full_amount
        and not project.fully_invested
    ):
        project.fully_invested = True
        project.close_date = datetime.now()

    await session.commit()
    await session.refresh(project)
    return project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),  # noqa: B008
):
    """Удалить проект."""
    project = await get_project_or_404(project_id, session)

    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERR_DELETE,
        )

    await session.delete(project)
    await session.commit()
    return project
