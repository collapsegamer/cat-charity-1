from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    app_title: str = "QRKot"
    description: str = (
        "Благотворительный фонд поддержки котиков QRKot"
    )
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"

    class Config:

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
