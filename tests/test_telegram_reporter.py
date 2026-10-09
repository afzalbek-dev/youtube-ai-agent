"""Unit tests for Telegram Reporter."""

from unittest.mock import patch, MagicMock
from youtube_ai_agent.core.telegram_reporter import TelegramReporter


def test_telegram_reporter_disabled_by_default(mock_settings):
    """Verify notification gracefully skips without error when disabled."""
    reporter = TelegramReporter(mock_settings)
    result = reporter.report_success("Topic", "test.mp4", 15.0, "Title")

    assert result.sent is False
    assert result.status == "skipped_notifications_disabled"


def test_telegram_reporter_sends_when_configured(mock_settings):
    """Verify message delivery via mocked HTTP request."""
    mock_settings.telegram_notifications_enabled = True
    mock_settings.telegram_bot_token = "12345:mock_bot_token"
    mock_settings.telegram_chat_id = "12345678"

    mock_resp = MagicMock()
    mock_resp.status_code = 200

    reporter = TelegramReporter(mock_settings)
    with patch("httpx.Client.post", return_value=mock_resp):
        res = reporter.report_success("Tech Topic", "video.mp4", 12.0, "Amazing Tech")
        assert res.sent is True
        assert res.status == "delivered"
