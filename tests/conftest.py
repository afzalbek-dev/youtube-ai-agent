"""Test fixtures and shared configuration for Pytest."""

import os
import shutil
import tempfile
from pathlib import Path
import pytest

from youtube_ai_agent.config import Settings
from youtube_ai_agent.core.scenario_generator import Scenario, Scene


@pytest.fixture
def temp_workspace():
    """Create an isolated temporary workspace directory for test execution."""
    tmp = tempfile.mkdtemp(prefix="test_yt_agent_")
    path = Path(tmp)
    output_dir = path / "output"
    temp_dir = path / "temp"
    output_dir.mkdir()
    temp_dir.mkdir()

    yield {
        "root": path,
        "output_dir": output_dir,
        "temp_dir": temp_dir,
    }

    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def mock_settings(temp_workspace):
    """Provide isolated settings instance using temp directories."""
    return Settings(
        app_env="test",
        log_level="DEBUG",
        dry_run=True,
        gemini_api_key=None,  # Tests should use offline fallback by default
        output_dir=temp_workspace["output_dir"],
        temp_dir=temp_workspace["temp_dir"],
        video_width=720,
        video_height=1280,
        video_fps=15,
        max_duration_seconds=30,
        default_scene_duration_seconds=2,
        youtube_upload_enabled=False,
        telegram_notifications_enabled=False,
    )


@pytest.fixture
def sample_scenario():
    """Provide a valid test scenario."""
    scenes = [
        Scene(
            scene_number=1,
            duration_seconds=2.0,
            narration="Hook narration test scene 1",
            visual_description="Opening visual graphic",
            text_overlay="TEST HOOK",
        ),
        Scene(
            scene_number=2,
            duration_seconds=2.0,
            narration="Insight narration test scene 2",
            visual_description="Insight infographic",
            text_overlay="KEY POINT",
        ),
    ]
    return Scenario(
        topic="AI Testing in 2026",
        target_duration=4.0,
        hook="Hook test statement",
        scenes=scenes,
        call_to_action="Follow for more",
        is_fallback=True,
        provider="test_fixture",
    )
