"""Unit tests for Quality Inspector."""

import pytest
from pathlib import Path
from unittest.mock import patch
from youtube_ai_agent.core.quality_inspector import QualityInspector


def test_quality_inspector_nonexistent_file(mock_settings):
    """Verify FileNotFoundError on non-existent media file."""
    inspector = QualityInspector(mock_settings)
    with pytest.raises(FileNotFoundError):
        inspector.inspect(Path("/tmp/does_not_exist_xyz.mp4"))


def test_quality_inspector_aspect_ratio_failure(mock_settings, temp_workspace):
    """Verify rejection of horizontal (16:9) video when 9:16 is required."""
    fake_video = temp_workspace["output_dir"] / "fake_horizontal.mp4"
    fake_video.touch()

    inspector = QualityInspector(mock_settings)
    # Mock metadata returning 1920x1080 horizontal
    mock_meta = {"duration": 10.0, "width": 1920, "height": 1080, "has_audio": True}
    
    with patch.object(inspector, "_get_media_metadata", return_value=mock_meta), \
         patch.object(inspector, "_detect_black_frames", return_value=0.01), \
         patch.object(inspector, "_detect_duplicate_frames", return_value=0.05):
        report = inspector.inspect(fake_video)
        assert report.is_valid is False
        assert any("aspect ratio" in f.lower() for f in report.failures)


def test_quality_inspector_success(mock_settings, temp_workspace):
    """Verify validation passes for valid vertical video with audio."""
    fake_video = temp_workspace["output_dir"] / "fake_vertical.mp4"
    fake_video.touch()

    inspector = QualityInspector(mock_settings)
    mock_meta = {
        "duration": 12.0,
        "width": mock_settings.video_width,
        "height": mock_settings.video_height,
        "has_audio": True,
    }

    with patch.object(inspector, "_get_media_metadata", return_value=mock_meta), \
         patch.object(inspector, "_detect_black_frames", return_value=0.02), \
         patch.object(inspector, "_detect_duplicate_frames", return_value=0.05):
        report = inspector.inspect(fake_video)
        assert report.is_valid is True
        assert len(report.failures) == 0
        assert report.duration_seconds == 12.0
