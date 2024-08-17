from pydantic import AnyHttpUrl, validator
from typing import List, Union, Optional
from pydantic_settings import BaseSettings


import os


class Settings(BaseSettings):
    # Application settings
    app_name: str = "Staff Eats Project"
    version: str = "1.0.0"


    refresh_token_expire_minutes: int = 60*24*10
    access_token_expire_minutes: int = 60*24*10
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    jwt_refresh_secret_key: str = os.getenv("JWT_REFRESH_SECRET_KEY")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM")
    admin_token_password: str = os.getenv("ADMIN_TOKEN_PASSWORD")
    bottoken :str = os.getenv("BOTTOKEN")
    frontbaseurl :str = os.getenv("FRONTBASEURL")
    backend_token :str = os.getenv("BACKEND_TOKEN")


    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

    # Security settings


    class Config:
        env_file = ".env"  # Specify the environment file to load


# Initialize settings
settings = Settings()
