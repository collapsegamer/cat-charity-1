from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.donation import DonationCreate, DonationDB, DonationResponse
from app.services.investments import invest

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True
)
async def get_donations(session: SessionDep):
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationResponse,
    response_model_exclude_none=True
)
async def create_donation(donation: DonationCreate, session: SessionDep):
    donation = await donation_crud.create(donation, session)
    projects = await charity_project_crud.get_open(session)
    modified = invest(target=donation, sources=projects)
    session.add_all(modified)
    await session.commit()
    await session.refresh(donation)
    return donation