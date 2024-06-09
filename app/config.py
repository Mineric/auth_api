from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_TITLE: str = "User Management API"
    APP_DESCRIPTION: str = "Basic User Authenticattion API for Technical Test"
    APP_VERSION: str = "1.0.0"

settings = Settings()
