from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.constants import APP_TITLE, DATABASE_URL, DESCRIPTION


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    app_title: str = APP_TITLE
    description: str = DESCRIPTION
    database_url: Optional[str] = DATABASE_URL


settings = Settings()
