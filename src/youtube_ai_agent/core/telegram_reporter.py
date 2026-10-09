"""Telegram Reporter module for pipeline progress and alert notifications."""

import logging
from typing import Optional
import httpx
from pydantic import BaseModel

from youtube_ai_agent.config import Settings
from youtube_ai_agent.exceptions import NotificationError

logger = logging.getLogger(__name__)


class NotificationResult(BaseModel):
    """Result of sending a status notification."""
    sent: bool
    status: str
    message_preview: str


class TelegramReporter:
    """Sends lifecycle alerts and failure notifications via Telegram Bot API."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.bot_token = settings.telegram_bot_token
        self.chat_id = settings.telegram_chat_id
        self.enabled = settings.telegram_notifications_enabled and bool(self.bot_token and self.chat_id)

    def report_success(self, topic: str, video_path: str, duration: float, title: str) -> NotificationResult:
        """Send a success notification for completed video creation."""
        text = (
            f"🎬 *YouTube AI Agent — Video Ready!*\n\n"
            f"📌 *Topic:* `{topic}`\n"
            f"⏱ *Duration:* {duration:.1f}s\n"
            f"🏷 *Title:* {title}\n"
            f"📁 *File:* `{video_path}`\n\n"
            f"✅ Quality inspection passed successfully."
        )
        return self._send_message(text)

    def report_failure(self, topic: str, stage: str, error_message: str) -> NotificationResult:
        """Send an urgent error report if pipeline fails."""
        text = (
            f"⚠️ *YouTube AI Agent — Pipeline Error*\n\n"
            f"📌 *Topic:* `{topic}`\n"
            f"❌ *Stage:* `{stage}`\n"
            f"🚨 *Details:* `{error_message[:200]}`\n\n"
            f"Check local logs for complete traceback."
        )
        return self._send_message(text)

    def _send_message(self, text: str) -> NotificationResult:
        """Send markdown text message to Telegram channel or chat."""
        if not self.enabled:
            logger.info(f"[TELEGRAM LOCAL LOG] Notification skipped (not configured):\n{text}")
            return NotificationResult(
                sent=False,
                status="skipped_notifications_disabled",
                message_preview=text[:60],
            )

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown",
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                resp = client.post(url, json=payload)
                if resp.status_code == 200:
                    logger.info("Telegram notification delivered successfully.")
                    return NotificationResult(sent=True, status="delivered", message_preview=text[:60])
                else:
                    logger.warning(f"Telegram API responded with HTTP {resp.status_code}: {resp.text}")
                    return NotificationResult(sent=False, status=f"api_error_{resp.status_code}", message_preview=text[:60])
        except Exception as e:
            logger.error(f"Failed to deliver Telegram notification: {e}")
            return NotificationResult(sent=False, status=f"network_exception_{e}", message_preview=text[:60])
