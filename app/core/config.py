from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Gym Management API"
    DATABASE_URL: str = "postgresql://gym_user:gym_password@db:5432/gym_db"
    REDIS_URL: str = "redis://redis:6379/0"
    JWT_SECRET: str = "troque-por-uma-chave-segura-de-32-caracteres"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()