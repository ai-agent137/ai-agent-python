from functools import  lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = Field(default="AI Agent Course API")
    app_env: str = Field(default="development")
    app_version: str = Field(default="0.1.0")
    api_v1_prefix: str = Field(default="/api/v1")
    debug: bool = Field(default=True)

    default_model: str = Field(default="deepseek-chat")
    supported_models: str = Field(default="deepseek-chat,qwen-plus,gpt-4o-mini")

    app_api_key: str = Field(default="dev-api-key-123")

    database_url: str = Field(
        default= "postgresql+asyncpg://postgres:123456@localhost:5432/ai_agent_course"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def supported_model_list(self) -> list[str]:
        return [
            model.strip()
            for model in self.supported_models.split(",")
            if model.strip()
        ]
        
@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()        