"""Unit tests for Scenario Generator with offline fallback and mock API."""

import pytest
from unittest.mock import patch, MagicMock
from youtube_ai_agent.core.scenario_generator import ScenarioGenerator


def test_scenario_offline_fallback(mock_settings):
    """Verify offline fallback scenario generation produces structured scenes."""
    generator = ScenarioGenerator(mock_settings)
    scenario = generator.generate("Quantum Computing Breakthrough", target_duration=9.0)

    assert scenario.topic == "Quantum Computing Breakthrough"
    assert scenario.is_fallback is True
    assert scenario.provider == "offline_fallback"
    assert len(scenario.scenes) == 3
    assert scenario.total_duration == pytest.approx(9.0, 0.1)
    assert scenario.scenes[0].text_overlay is not None


def test_scenario_gemini_api_success(mock_settings):
    """Verify Gemini API response parsing when key is provided."""
    mock_settings.gemini_api_key = "fake_test_key"
    generator = ScenarioGenerator(mock_settings)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": "Quantum computers just achieved quantum advantage in 2026."}]
                }
            }
        ]
    }

    with patch("httpx.Client.post", return_value=mock_response):
        scenario = generator.generate("Quantum Tech", target_duration=6.0)
        assert scenario.is_fallback is False
        assert scenario.provider == "gemini_api"
        assert len(scenario.scenes) == 3
        assert "Quantum" in scenario.scenes[1].narration
