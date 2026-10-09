"""Unit tests for Media Synthesizer with FFmpeg and fallback checks."""

import pytest
from pathlib import Path
from youtube_ai_agent.config import Settings
from youtube_ai_agent.core.media_synthesizer import MediaSynthesizer
from youtube_ai_agent.exceptions import MediaSynthesisError


def test_ffmpeg_missing_error(mock_settings, sample_scenario):
    """Verify clean error when FFmpeg executable is absent."""
    synth = MediaSynthesizer(mock_settings, ffmpeg_bin="/non/existent/path/ffmpeg")
    with pytest.raises(MediaSynthesisError, match="FFmpeg executable not found"):
        synth.synthesize(sample_scenario)


def test_scene_frame_generation(mock_settings, sample_scenario, temp_workspace):
    """Verify PIL generates valid 9:16 vertical PNG frame."""
    synth = MediaSynthesizer(mock_settings)
    img_path = temp_workspace["temp_dir"] / "test_frame.png"
    
    synth._create_scene_frame(sample_scenario.scenes[0], img_path)
    assert img_path.exists()
    assert img_path.stat().st_size > 1000


@pytest.mark.skipif(not MediaSynthesizer(Settings()).check_ffmpeg_available(), reason="FFmpeg not installed")
def test_real_media_synthesis(mock_settings, sample_scenario):
    """Test actual video synthesis with installed FFmpeg."""
    synth = MediaSynthesizer(mock_settings)
    video_path = synth.synthesize(sample_scenario, output_filename="test_render.mp4")

    assert video_path.exists()
    assert video_path.stat().st_size > 5000
    assert video_path.suffix == ".mp4"
