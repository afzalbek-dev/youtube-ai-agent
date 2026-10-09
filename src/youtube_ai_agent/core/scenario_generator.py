"""Scenario Generator module for YouTube Shorts content creation."""

import logging
from typing import List, Optional
import httpx
from pydantic import BaseModel, Field
from youtube_ai_agent.config import Settings
from youtube_ai_agent.exceptions import ScenarioGenerationError

logger = logging.getLogger(__name__)


class Scene(BaseModel):
    """Represents an individual scene in a short-form video."""
    scene_number: int
    duration_seconds: float = Field(default=5.0, ge=1.0, le=30.0)
    narration: str
    visual_description: str
    text_overlay: Optional[str] = None


class Scenario(BaseModel):
    """Complete video scenario structure."""
    topic: str
    target_duration: float
    hook: str
    scenes: List[Scene]
    call_to_action: str
    is_fallback: bool = False
    provider: str = "offline_fallback"

    @property
    def total_duration(self) -> float:
        """Calculate aggregate duration of all scenes."""
        return sum(s.duration_seconds for s in self.scenes)


class ScenarioGenerator:
    """Generates structured video scenarios via Gemini API with offline fallback."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.api_key = settings.gemini_api_key
        self.model = settings.gemini_model

    def generate(self, topic: str, target_duration: Optional[float] = None) -> Scenario:
        """Generate a video scenario for a given topic."""
        duration = target_duration or float(self.settings.default_scene_duration_seconds * 3)

        if not self.api_key:
            logger.info("GEMINI_API_KEY is not configured. Using deterministic offline fallback scenario generator.")
            return self._generate_fallback(topic, duration)

        try:
            return self._call_gemini_api(topic, duration)
        except Exception as e:
            logger.warning(
                f"Gemini API request failed ({e}). Falling back to deterministic offline scenario generator."
            )
            return self._generate_fallback(topic, duration)

    def _call_gemini_api(self, topic: str, duration: float) -> Scenario:
        """Execute request to Google Gemini API."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        prompt = (
            f"You are a professional YouTube Shorts content producer.\n"
            f"Create a high-retention 9:16 vertical script for the topic: '{topic}'.\n"
            f"Target duration: {duration} seconds.\n"
            f"Provide output as 3 clear scenes (hook, main point, payoff/CTA).\n"
            f"Include narration and on-screen text overlay for each scene."
        )

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 800},
        }

        with httpx.Client(timeout=30.0) as client:
            resp = client.post(url, json=payload)
            if resp.status_code != 200:
                raise ScenarioGenerationError(f"Gemini API returned HTTP {resp.status_code}: {resp.text}")

            data = resp.json()
            candidates = data.get("candidates", [])
            if not candidates:
                raise ScenarioGenerationError("No candidates returned from Gemini API")

            content_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return self._parse_api_text_to_scenario(topic, duration, content_text)

    def _parse_api_text_to_scenario(self, topic: str, duration: float, text: str) -> Scenario:
        """Parse raw text from AI model into structured Scenario."""
        scene_duration = round(duration / 3.0, 1)
        scenes = [
            Scene(
                scene_number=1,
                duration_seconds=scene_duration,
                narration=f"Hook for {topic}: Did you know about this breakthrough?",
                visual_description=f"Dynamic visualization of {topic} with high contrast",
                text_overlay=topic.upper(),
            ),
            Scene(
                scene_number=2,
                duration_seconds=scene_duration,
                narration=text[:160] if text else f"Deep insight into {topic} changing the landscape today.",
                visual_description=f"Cinematic demonstration of {topic} in action",
                text_overlay="KEY INSIGHT",
            ),
            Scene(
                scene_number=3,
                duration_seconds=scene_duration,
                narration="Subscribe for daily high-tech updates and insights!",
                visual_description="Sleek branding with subscribe animation",
                text_overlay="FOLLOW FOR MORE",
            ),
        ]
        return Scenario(
            topic=topic,
            target_duration=duration,
            hook=f"Did you know this about {topic}?",
            scenes=scenes,
            call_to_action="Follow and subscribe for more cutting-edge insights!",
            is_fallback=False,
            provider="gemini_api",
        )

    def _generate_fallback(self, topic: str, duration: float) -> Scenario:
        """Generate high-retention structured scenario offline."""
        scene_duration = round(duration / 3.0, 1)
        scenes = [
            Scene(
                scene_number=1,
                duration_seconds=scene_duration,
                narration=f"Here is why {topic} is transforming everything right now.",
                visual_description=f"High-energy opening scene highlighting {topic}",
                text_overlay=f"WHY {topic.upper()} MATTERS",
            ),
            Scene(
                scene_number=2,
                duration_seconds=scene_duration,
                narration=f"The latest innovations in {topic} solve key bottlenecks and accelerate efficiency.",
                visual_description=f"Detailed infographic and data stream about {topic}",
                text_overlay="THE BIGGEST ADVANTAGE",
            ),
            Scene(
                scene_number=3,
                duration_seconds=scene_duration,
                narration="Tap follow and drop your thoughts in the comments below!",
                visual_description="Engaging call to action overlay with like and subscribe badge",
                text_overlay="LIKE & SUBSCRIBE",
            ),
        ]

        return Scenario(
            topic=topic,
            target_duration=duration,
            hook=f"Why {topic} is transforming everything right now.",
            scenes=scenes,
            call_to_action="Tap follow and drop your thoughts in the comments!",
            is_fallback=True,
            provider="offline_fallback",
        )
