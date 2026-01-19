from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    openai_api_key: str = Field(
        ...,
        description="OpenAI API key for authentication",
        min_length=1,
    )
    openai_model: str = Field(
        default="gpt-4o",
        description="The GPT model to use for resume analysis",
    )
    openai_temperature: float = Field(
        default=0.3,
        ge=0.0,
        le=2.0,
        description="Temperature for response generation (lower = more deterministic)",
    )
    openai_max_tokens: int = Field(
        default=2000,
        ge=100,
        le=16000,
        description="Maximum tokens in the response",
    )
    
    log_level: str = Field(
        default="INFO",
        description="Application logging level",
    )
    prompts_dir: Path = Field(
        default=Path("prompts"),
        description="Directory containing prompt templates",
    )
    
    @property
    def scoring_prompt_path(self) -> Path:
        return self.prompts_dir / "scoring_prompt.txt"


@lru_cache
def get_settings() -> Settings:
    return Settings()
