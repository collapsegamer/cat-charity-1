"""Модуль с настройками приложения."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Параметры конфигурации приложения."""

    app_title: str = "QRKot"
    description: str = (
        "Благотворительный фонд поддержки котиков QRKot"
    )
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"

    class Config:
        """Настройки загрузки переменных окружения."""

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
