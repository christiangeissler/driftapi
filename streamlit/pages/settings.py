from typing import Set

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Parameters to be loaded from Environment Variables in .env file"""

    # Database
    driftapi_root_path: str = "http://localhost:8001"

    class Config:
        env_prefix = "STREAMLIT_"
        env_file = ".env"