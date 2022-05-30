import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Main settings"""

    env: str = os.getenv("ENV", "production")
    database_url: str = os.getenv("DATABASE_URL", "")

    class Config:
        """Retrieves config from .env file if it exists"""

        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Retrieves the fastapi settings. lru_cache is used for caching

    Returns:
        Settings: _description_
    """
    return Settings()
