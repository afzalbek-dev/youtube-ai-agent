"""Metadata Generator module for YouTube Shorts SEO, titles, and hashtags."""

import logging
from typing import List
from pydantic import BaseModel, Field

from youtube_ai_agent.config import Settings
from youtube_ai_agent.core.scenario_generator import Scenario

logger = logging.getLogger(__name__)


class VideoMetadata(BaseModel):
    """Complete metadata for a YouTube video upload."""
    title: str
    description: str
    tags: List[str]
    hashtags: List[str]
    category_id: str = "28"  # 28 = Science & Technology
    privacy_status: str = "private"


class MetadataGenerator:
    """Generates engaging titles, descriptions, and hashtags for YouTube Shorts."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def generate(self, scenario: Scenario) -> VideoMetadata:
        """Generate optimized metadata based on video scenario."""
        clean_topic = scenario.topic.strip().title()

        # Catchy short-form title (< 60 characters for mobile display)
        title_candidates = [
            f"{clean_topic} Will Change EVERYTHING! 🤯 #Shorts",
            f"The Hidden Truth Behind {clean_topic} #Shorts",
            f"Why {clean_topic} Matters in 2026 ⚡ #Shorts",
        ]
        title = title_candidates[0]
        if len(title) > 95:
            title = f"{clean_topic[:70]} #Shorts"

        # Relevant hashtags
        slug = "".join(word for word in clean_topic.split() if word.isalnum())
        hashtags = ["#Shorts", "#Tech", "#Innovation", f"#{slug}", "#Trending"]

        # Rich description
        description_lines = [
            f"{scenario.hook}",
            "",
            f"In this short breakdown, explore the reality of {clean_topic}.",
            "",
            "Key Insights Covered:",
        ]
        for scene in scenario.scenes:
            description_lines.append(f"• {scene.narration[:100]}")

        description_lines.extend([
            "",
            scenario.call_to_action,
            "",
            " ".join(hashtags),
        ])
        description = "\n".join(description_lines)

        tags = [
            clean_topic.lower(),
            "shorts",
            "youtube shorts",
            "tech trends",
            "future tech",
            "education",
            "ai agent",
        ]

        logger.info(f"Generated metadata: Title='{title}' | Tags={len(tags)}")

        return VideoMetadata(
            title=title,
            description=description,
            tags=tags,
            hashtags=hashtags,
            category_id="28",
            privacy_status=self.settings.youtube_privacy_status,
        )
