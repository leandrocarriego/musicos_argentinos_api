from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_DB_NAME: str
    DB_URI: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

settings = Settings()

