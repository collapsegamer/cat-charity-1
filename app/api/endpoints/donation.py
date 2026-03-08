from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationCreateResponse, DonationFullInfoDB
from app.services.investing import invest

router = APIRouter(prefix="/donation", tags=["donations"])


@router.get(
    "/",
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
)
async def get_donations(session: AsyncSession = Depends(get_async_session)):
    return await donation_crud.get_all(session)


@router.post(
    "/",
    response_model=DonationCreateResponse,
    response_model_exclude_none=True,
)
async def create_donation(
    data: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    donation = Donation(**data.model_dump(exclude_unset=True))
    await donation_crud.create(session, donation)

    await invest(session, donation)

    await session.commit()
    await session.refresh(donation)
    return donation
