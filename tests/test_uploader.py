"""Unit tests for YouTube Uploader safety gates."""

import pytest
from pathlib import Path
from youtube_ai_agent.core.metadata_generator import VideoMetadata
from youtube_ai_agent.core.youtube_uploader import YouTubeUploader
from youtube_ai_agent.exceptions import UploadError


@pytest.fixture
def sample_metadata():
    return VideoMetadata(
        title="Test Title #Shorts",
        description="Test Description",
        tags=["tech", "ai"],
        hashtags=["#Shorts"],
    )


def test_uploader_dry_run_safety(mock_settings, sample_metadata, temp_workspace):
    """Verify uploader always defaults to dry-run when upload is disabled."""
    fake_video = temp_workspace["output_dir"] / "ready_video.mp4"
    fake_video.touch()

    uploader = YouTubeUploader(mock_settings)
    result = uploader.upload(fake_video, sample_metadata, force_upload=False)

    assert result.is_dry_run is True
    assert result.status == "dry_run_completed"
    assert "preview" in result.video_url


def test_uploader_requires_client_secrets_when_forced(mock_settings, sample_metadata, temp_workspace):
    """Verify forced upload raises error if OAuth client secrets file is missing."""
    fake_video = temp_workspace["output_dir"] / "ready_video.mp4"
    fake_video.touch()

    mock_settings.youtube_upload_enabled = True
    mock_settings.dry_run = False
    mock_settings.youtube_client_secrets_file = "non_existent_secrets.json"

    uploader = YouTubeUploader(mock_settings)
    with pytest.raises(UploadError, match="client secrets file.*not found"):
        uploader.upload(fake_video, sample_metadata, force_upload=True)
