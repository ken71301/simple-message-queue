from pydantic_settings import BaseSettings

class Config(BaseSettings):
    redis_url: str = 'redis://redis:6379'