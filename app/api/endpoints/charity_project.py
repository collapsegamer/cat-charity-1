from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_project_can_be_deleted,
    check_project_can_be_updated,
    check_project_exists
)
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.investments import invest

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_project(session: SessionDep):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: SessionDep
):
    await check_name_duplicate(charity_project.name, session)
    project = await charity_project_crud.create(charity_project, session)
    donations = await donation_crud.get_open(session)
    modified = invest(target=project, sources=donations)
    session.add_all(modified)
    await session.commit()
    await session.refresh(project)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: SessionDep
):
    project = await check_project_exists(project_id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    check_project_can_be_updated(project, obj_in)
    project = await charity_project_crud.update(project, obj_in, session)
    project.recalculate_state()
    await session.commit()
    await session.refresh(project)
    return project


@router.delete('/{project_id}', response_model=CharityProjectDB)
async def delete_charity_project(project_id: int, session: SessionDep):
    project = await check_project_exists(project_id, session)
    check_project_can_be_deleted(project)
    project = await charity_project_crud.remove(project, session)
    return project
