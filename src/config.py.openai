# File: src/config.py
"""
Configuration management using Pydantic-Settings for a modern, robust setup.
This version is cleaned up to be a best-in-class reference.
"""
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    """
    Application configuration with automatic environment variable loading.
    Defines a clear, type-safe structure for all application settings.
    """
    
    # This tells Pydantic-Settings to load from a .env file,
    # use a "CONTEXT7_" prefix as a fallback, and be case-insensitive.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="CONTEXT7_",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Required: Will raise an error if not found.
    # It will first look for OPENAI_API_KEY, then CONTEXT7_OPENAI_API_KEY.
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    
    # Optional fields with sensible defaults.
    openai_base_url: str = Field(
        default="https://api.openai.com/v1",
        description="OpenAI API base URL"
    )
    openai_model: str = Field(
        default="gpt-4o-mini",
        description="OpenAI model to use (e.g., gpt-4o-mini, gpt-4-turbo)"
    )
    
    # Use pathlib.Path for robust, platform-agnostic path management.
    history_path: Path = Field(
        default_factory=lambda: Path("data/history.json"),
        description="Path to conversation history file"
    )
    max_history: int = Field(
        default=50,
        description="Maximum conversation history entries per conversation thread"
    )
    
    def __init__(self, **kwargs):
        """Ensures required directories exist upon initialization."""
        super().__init__(**kwargs)
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Proactively creates the data directory to prevent errors on first run."""
        self.history_path.parent.mkdir(parents=True, exist_ok=True)

# Create a single, global config instance for easy importing across the application.
config = Config()
