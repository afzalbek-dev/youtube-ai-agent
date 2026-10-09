"""Configuration management using Pydantic and python-dotenv."""

import os
from functools import lru_cache
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file if it exists
load_dotenv()

class Settings(BaseModel):
    """Application settings with environment variable fallbacks."""

    app_env: str = Field(default_factory=lambda: os.getenv("APP_ENV", "development"))
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    dry_run: bool = Field(default_factory=lambda: os.getenv("DRY_RUN", "true").lower() in ("1", "true", "yes"))

    # Gemini API
    gemini_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY") or None)
    gemini_model: str = Field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))

    # Video parameters
    output_dir: Path = Field(default_factory=lambda: Path(os.getenv("OUTPUT_DIR", "output")))
    temp_dir: Path = Field(default_factory=lambda: Path(os.getenv("TEMP_DIR", "temp")))
    video_width: int = Field(default_factory=lambda: int(os.getenv("VIDEO_WIDTH", "1080")))
    video_height: int = Field(default_factory=lambda: int(os.getenv("VIDEO_HEIGHT", "1920")))
    video_fps: int = Field(default_factory=lambda: int(os.getenv("VIDEO_FPS", "30")))
    max_duration_seconds: int = Field(default_factory=lambda: int(os.getenv("MAX_DURATION_SECONDS", "60")))
    default_scene_duration_seconds: int = Field(
        default_factory=lambda: int(os.getenv("DEFAULT_SCENE_DURATION_SECONDS", "5"))
    )

    # Quality Inspection Thresholds
    max_black_frame_ratio: float = Field(
        default_factory=lambda: float(os.getenv("MAX_BLACK_FRAME_RATIO", "0.08"))
    )
    similarity_hash_threshold: int = Field(
        default_factory=lambda: int(os.getenv("SIMILARITY_HASH_THRESHOLD", "5"))
    )
    min_audio_duration_ratio: float = Field(
        default_factory=lambda: float(os.getenv("MIN_AUDIO_DURATION_RATIO", "0.85"))
    )

    # Telegram Bot
    telegram_bot_token: Optional[str] = Field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN") or None)
    telegram_chat_id: Optional[str] = Field(default_factory=lambda: os.getenv("TELEGRAM_CHAT_ID") or None)
    telegram_notifications_enabled: bool = Field(
        default_factory=lambda: os.getenv("TELEGRAM_NOTIFICATIONS_ENABLED", "false").lower() in ("1", "true", "yes")
    )

    # YouTube Data API
    youtube_upload_enabled: bool = Field(
        default_factory=lambda: os.getenv("YOUTUBE_UPLOAD_ENABLED", "false").lower() in ("1", "true", "yes")
    )
    youtube_client_secrets_file: str = Field(
        default_factory=lambda: os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "client_secrets.json")
    )
    youtube_token_file: str = Field(
        default_factory=lambda: os.getenv("YOUTUBE_TOKEN_FILE", "token.json")
    )
    youtube_privacy_status: str = Field(
        default_factory=lambda: os.getenv("YOUTUBE_PRIVACY_STATUS", "private")
    )

    def ensure_directories(self) -> None:
        """Ensure necessary output and temporary directories exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)


@lru_cache()
def get_settings() -> Settings:
    """Retrieve cached instance of application settings."""
    settings = Settings()
    settings.ensure_directories()
    return settings
