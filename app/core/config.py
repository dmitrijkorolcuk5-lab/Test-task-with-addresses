from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_URL: str
    REDIS_URL: str
    SHIPENGINE_API_KEY: str
    
    APP_HOST: str = "0.0.0.0" 
    APP_PORT: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()