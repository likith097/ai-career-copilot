from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Career Copilot"
    openai_api_key: str | None = None
    llm_provider: str = "mock"  # mock or openai

    class Config:
        env_file = ".env"


settings = Settings()
