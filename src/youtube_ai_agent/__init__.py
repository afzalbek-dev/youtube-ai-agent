"""YouTube AI Agent.

Autonomous pipeline for YouTube Shorts generation, quality inspection, and publishing.
"""

__version__ = "1.0.0"
__author__ = "Afzalbek"

from youtube_ai_agent.config import Settings, get_settings
from youtube_ai_agent.pipeline import VideoPipeline

__all__ = ["Settings", "get_settings", "VideoPipeline", "__version__"]
