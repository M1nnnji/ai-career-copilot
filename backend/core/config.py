"""환경변수 설정 — .env / docker-compose에서 주입."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://career:career@localhost:5432/career_copilot"
    kafka_bootstrap_servers: str = "localhost:9092"

    llm_provider: str = "openai"
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    api_host: str = "0.0.0.0"
    api_port: int = 8000


settings = Settings()
