from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investing import invest

router = APIRouter(prefix="/charity_project", tags=["charity_projects"])


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_projects(session: AsyncSession = Depends(get_async_session)):
    return await charity_project_crud.get_all(session)


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def create_project(
    data: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    if await charity_project_crud.get_by_name(session, data.name):
        raise HTTPException(400, "Проект с таким именем уже существует!")

    project = CharityProject(**data.model_dump())
    await charity_project_crud.create(session, project)

    await invest(session, project)

    await session.commit()
    await session.refresh(project)
    return project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def update_project(
    project_id: int,
    data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await charity_project_crud.get(session, project_id)
    if not project:
        raise HTTPException(404, "The project does not exist")

    if project.fully_invested:
        raise HTTPException(400, "Закрытый проект нельзя редактировать!")

    payload = data.model_dump(exclude_unset=True)

    if "name" in payload:
        other = await charity_project_crud.get_by_name(session, payload["name"])
        if other and other.id != project.id:
            raise HTTPException(400, "Проект с таким именем уже существует!")

    if "full_amount" in payload and payload["full_amount"] < project.invested_amount:
        raise HTTPException(
            400,
            "Нелья установить значение full_amount меньше уже вложенной суммы.",
        )

    for field, value in payload.items():
        setattr(project, field, value)

    if project.invested_amount == project.full_amount:
        project.fully_invested = True
        project.close_date = datetime.utcnow()

    await session.commit()
    await session.refresh(project)
    return project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await charity_project_crud.get(session, project_id)
    if not project:
        raise HTTPException(404, "The project does not exist")

    if project.invested_amount > 0 or project.fully_invested:
        raise HTTPException(
            400,
            "В проект были внесены средства, не подлежит удалению!",
        )

    await charity_project_crud.delete(session, project)
    await session.commit()
    return project
