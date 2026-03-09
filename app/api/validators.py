from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import (
    DELETE_INVESTED_PROJECT,
    PROJECT_EDIT_FULL_AMOUNT,
    PROJECT_FULLY_INVESTED,
    PROJECT_NAME_EXIST,
    PROJECT_NOT_FOUND
)
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name,
        session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_NAME_EXIST,
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=PROJECT_NOT_FOUND
        )
    return project


def check_project_can_be_updated(
        project: CharityProject,
        obj_in: CharityProjectUpdate,
):
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_FULLY_INVESTED
        )
    if (
        obj_in.full_amount is not None and
        obj_in.full_amount < project.invested_amount
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_EDIT_FULL_AMOUNT
        )


def check_project_can_be_deleted(project):
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=DELETE_INVESTED_PROJECT
        )
