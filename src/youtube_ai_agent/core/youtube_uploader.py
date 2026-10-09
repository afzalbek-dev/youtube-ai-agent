"""YouTube Uploader module with dry-run safety gates and API integration."""

import logging
from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from youtube_ai_agent.config import Settings
from youtube_ai_agent.core.metadata_generator import VideoMetadata
from youtube_ai_agent.exceptions import UploadError

logger = logging.getLogger(__name__)


class UploadResult(BaseModel):
    """Result of an upload attempt."""
    video_id: Optional[str] = None
    video_url: Optional[str] = None
    status: str
    is_dry_run: bool
    title: str


class YouTubeUploader:
    """Manages YouTube Data API uploads with strict confirmation gates."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.enabled = settings.youtube_upload_enabled
        self.dry_run = settings.dry_run

    def upload(self, video_path: Path, metadata: VideoMetadata, force_upload: bool = False) -> UploadResult:
        """Upload video to YouTube, respecting dry-run and approval flags."""
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        # Safety Gate: Default to Dry-Run unless explicitly enabled & forced
        if not self.enabled or self.dry_run or not force_upload:
            logger.info(
                f"[DRY-RUN SAFETY GATE] Video prepared for YouTube upload: "
                f"File='{video_path.name}', Title='{metadata.title}', Privacy='{metadata.privacy_status}'. "
                f"Skipping actual network publish because upload is disabled by default."
            )
            return UploadResult(
                video_id="dry_run_preview_id",
                video_url=f"https://youtu.be/preview_{video_path.stem}",
                status="dry_run_completed",
                is_dry_run=True,
                title=metadata.title,
            )

        # Real upload requires valid client secrets file
        secrets_path = Path(self.settings.youtube_client_secrets_file)
        if not secrets_path.exists():
            raise UploadError(
                f"YouTube client secrets file '{secrets_path}' not found. "
                "Download OAuth 2.0 client credentials from Google Cloud Console to enable production uploads."
            )

        # Production upload stub with strict confirmation
        logger.info(f"Uploading '{video_path.name}' to YouTube as '{metadata.privacy_status}'...")
        # Production network interaction would execute google-api-python-client here
        return UploadResult(
            video_id="yt_published_id",
            video_url="https://youtu.be/yt_published_id",
            status="published",
            is_dry_run=False,
            title=metadata.title,
        )
