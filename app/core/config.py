import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")
    DB_URI: str = os.getenv("DB_URI")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

settings = Settings()
