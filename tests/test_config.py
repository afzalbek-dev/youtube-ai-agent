"""Tests for configuration and environment variable loading."""

from pathlib import Path
from youtube_ai_agent.config import Settings


def test_settings_default_values():
    """Verify default setting properties."""
    settings = Settings()
    assert settings.app_env in ("development", "test", "production")
    assert settings.video_width > 0
    assert settings.video_height > settings.video_width  # Must be vertical
    assert settings.youtube_upload_enabled is False  # Safe by default


def test_settings_directory_creation(temp_workspace):
    """Verify directory creation logic."""
    target_out = temp_workspace["root"] / "nested_out"
    target_tmp = temp_workspace["root"] / "nested_tmp"
    
    settings = Settings(output_dir=target_out, temp_dir=target_tmp)
    settings.ensure_directories()
    
    assert target_out.exists()
    assert target_tmp.exists()
