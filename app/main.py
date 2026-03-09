from fastapi import FastAPI

from app.api.charity_project import router as charity_project_router
from app.api.donation import router as donation_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
)

app.include_router(charity_project_router)
app.include_router(donation_router)
