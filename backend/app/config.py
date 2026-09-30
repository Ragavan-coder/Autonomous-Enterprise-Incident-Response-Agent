import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/aira")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    FAST_MODE: bool = os.getenv("FAST_MODE", "True") == "True"
    MAX_TOOL_CALLS: int = 15
    MAX_AGENT_STEPS: int = 20
    MAX_RUNTIME_SECONDS: int = 120

settings = Settings()
