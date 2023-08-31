from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: int
    MONGODB_HOST: str
    MONGODB_PORT: str
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_DB_NAME: str
    DB_URI: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
