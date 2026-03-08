from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI CapTrack"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/aicaptrack"

    REDIS_URL: str = "redis://localhost:6379/0"

    HUGGINGFACE_API_URL: str = "https://huggingface.co/api"
    GITHUB_API_URL: str = "https://api.github.com"
    FUTURETOOLS_API_URL: str = "https://www.futuretools.io"

    LLM_API_KEY: str = ""
    LLM_API_URL: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-4"

    CACHE_TTL_CAPABILITIES: int = 3600
    CACHE_TTL_LLM_PARSE: int = 30 * 24 * 3600

    SCHEDULER_ENABLED: bool = True
    COLLECTION_INTERVAL_HOURS: int = 24

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
