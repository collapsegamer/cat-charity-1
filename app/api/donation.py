from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models import Donation
from app.schemas import DonationCreate, DonationDB, DonationFullInfoDB
from app.services.investment import invest_new_donation

router = APIRouter(
    prefix="/donation",
    tags=["donations"],
)

ERR_NOT_FOUND = "Пожертвование не найдено."


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),  # noqa: B008
):
    donation = Donation(**donation_in.model_dump())
    session.add(donation)

    await invest_new_donation(donation, session)

    await session.commit()
    await session.refresh(donation)
    return donation


@router.get(
    "/",
    response_model=list[DonationFullInfoDB],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),  # noqa: B008
):
    result = await session.execute(
        select(Donation).order_by(Donation.create_date)
    )
    return result.scalars().all()


@router.get(
    "/my",
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),  # noqa: B008
):
    result = await session.execute(
        select(Donation).order_by(Donation.create_date)
    )
    return result.scalars().all()


@router.patch("/{donation_id}")
async def patch_donation(
    donation_id: int,
):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=ERR_NOT_FOUND,
    )


@router.put("/{donation_id}")
async def put_donation(
    donation_id: int,
):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=ERR_NOT_FOUND,
    )


@router.delete("/{donation_id}")
async def delete_donation(
    donation_id: int,
):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=ERR_NOT_FOUND,
    )
