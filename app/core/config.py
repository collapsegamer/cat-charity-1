from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Благотворительный фонд поддержки котиков QRKot"
    app_description: str = "Сервис для поддержки котиков"
    app_version: str = "0.1.0"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
