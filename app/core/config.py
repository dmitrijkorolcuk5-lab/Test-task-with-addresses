from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_URL: str
    REDIS_URL: str
    SHIPENGINE_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()