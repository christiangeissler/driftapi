from typing import Set

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Parameters to be loaded from Environment Variables in .env file"""

    # API
    disable_openapi: bool = False
    root_path: str = None
    cors_allow_origins: Set[str] = None
    enable_racedisplay = True

    # Database
    database_url: str = "mongodb://localhost:27017/"
    database_name: str = "driftapi-test-db"

    class Config:
        env_prefix = "DRIFTAPI_"
        env_file = ".env"
