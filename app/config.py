from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_TOKEN: str = "your-secure-token"
    REDIS_URL: str = "redis://localhost:6379"
    RETRY_ATTEMPTS: int = 3
    RETRY_DELAY: int = 5
    BASE_URL: str = "https://dentalstall.com/shop/"
    
    class Config:
        env_file = ".env"

settings = Settings()
