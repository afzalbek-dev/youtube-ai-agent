"""End-to-end integration tests for VideoPipeline."""

import pytest
from pathlib import Path
from youtube_ai_agent.pipeline import VideoPipeline
from youtube_ai_agent.core.media_synthesizer import MediaSynthesizer


@pytest.mark.skipif(not MediaSynthesizer(None, None).check_ffmpeg_available(), reason="FFmpeg not available")
def test_full_pipeline_run_integration(mock_settings):
    """Execute complete end-to-end pipeline run from scenario to QC and dry-run upload."""
    pipeline = VideoPipeline(mock_settings)
    result = pipeline.run(
        topic="Neural Interfaces 2026",
        target_duration=4.0,
        output_filename="test_e2e_output.mp4",
        force_upload=False,
    )

    assert result.success is True
    assert Path(result.video_path).exists()
    assert result.quality_report.is_valid is True
    assert result.upload_result.is_dry_run is True
    assert "Neural Interfaces" in result.metadata.title
