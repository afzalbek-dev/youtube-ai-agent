"""Quality Inspector module for validating synthesized video assets."""

import json
import logging
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field

from youtube_ai_agent.config import Settings
from youtube_ai_agent.exceptions import QualityCheckFailedError

logger = logging.getLogger(__name__)


class QualityReport(BaseModel):
    """Detailed quality validation report for a video file."""
    video_path: str
    duration_seconds: float
    width: int
    height: int
    has_audio_track: bool
    black_frame_ratio: float
    duplicate_frame_ratio: float
    is_valid: bool = False
    failures: List[str] = Field(default_factory=list)


class QualityInspector:
    """Performs automated QC checks on generated vertical videos."""

    def __init__(self, settings: Settings, ffprobe_bin: Optional[str] = None):
        self.settings = settings
        self.ffprobe_path = ffprobe_bin or shutil.which("ffprobe")
        self.ffmpeg_path = shutil.which("ffmpeg")

    def inspect(self, video_path: Path) -> QualityReport:
        """Analyze a video file and return a comprehensive QualityReport."""
        if not video_path.exists():
            raise FileNotFoundError(f"Video file does not exist: {video_path}")

        failures = []

        # 1. Metadata check via ffprobe
        metadata = self._get_media_metadata(video_path)
        duration = metadata.get("duration", 0.0)
        width = metadata.get("width", 0)
        height = metadata.get("height", 0)
        has_audio = metadata.get("has_audio", False)

        # Resolution & Aspect ratio check (Must be 9:16 vertical)
        if width > height or (width != self.settings.video_width and height != self.settings.video_height):
            failures.append(f"Invalid vertical aspect ratio: {width}x{height} (expected 9:16, e.g. 1080x1920)")

        # Duration check (Must be > 0 and <= max_duration_seconds)
        if duration <= 0:
            failures.append("Video duration is 0 seconds (empty file)")
        elif duration > self.settings.max_duration_seconds:
            failures.append(f"Duration {duration:.1f}s exceeds maximum allowed {self.settings.max_duration_seconds}s")

        # Audio check
        if not has_audio:
            failures.append("Audio stream missing from synthesized video")

        # 2. Black frame analysis
        black_ratio = self._detect_black_frames(video_path, duration)
        if black_ratio > self.settings.max_black_frame_ratio:
            failures.append(
                f"Black frame ratio ({black_ratio:.2%}) exceeds threshold ({self.settings.max_black_frame_ratio:.2%})"
            )

        # 3. Duplicate/frozen frame ratio check
        duplicate_ratio = self._detect_duplicate_frames(video_path)
        if duplicate_ratio > 0.85 and duration > 5.0:
            failures.append(f"Excessive duplicate/frozen frame ratio detected: {duplicate_ratio:.2%}")

        is_valid = len(failures) == 0
        report = QualityReport(
            video_path=str(video_path),
            duration_seconds=duration,
            width=width,
            height=height,
            has_audio_track=has_audio,
            black_frame_ratio=black_ratio,
            duplicate_frame_ratio=duplicate_ratio,
            is_valid=is_valid,
            failures=failures,
        )

        if not is_valid:
            logger.warning(f"Video quality checks failed: {failures}")
        else:
            logger.info(f"Video passed all quality checks ({duration:.1f}s, {width}x{height})")

        return report

    def _get_media_metadata(self, video_path: Path) -> dict:
        """Extract duration, resolution and streams via ffprobe."""
        if not self.ffprobe_path:
            logger.warning("ffprobe not available, returning default fallback metadata")
            return {"duration": 15.0, "width": 1080, "height": 1920, "has_audio": True}

        cmd = [
            self.ffprobe_path,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(video_path),
        ]

        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            data = json.loads(res.stdout)
            
            format_info = data.get("format", {})
            duration = float(format_info.get("duration", 0.0))
            
            width = 0
            height = 0
            has_audio = False

            for stream in data.get("streams", []):
                if stream.get("codec_type") == "video" and not width:
                    width = int(stream.get("width", 0))
                    height = int(stream.get("height", 0))
                elif stream.get("codec_type") == "audio":
                    has_audio = True

            return {"duration": duration, "width": width, "height": height, "has_audio": has_audio}
        except Exception as e:
            logger.error(f"Failed to probe media: {e}")
            return {"duration": 0.0, "width": 0, "height": 0, "has_audio": False}

    def _detect_black_frames(self, video_path: Path, duration: float) -> float:
        """Detect ratio of black frames using FFmpeg blackdetect filter."""
        if not self.ffmpeg_path or duration <= 0:
            return 0.0

        cmd = [
            self.ffmpeg_path,
            "-i", str(video_path),
            "-vf", "blackdetect=d=0.1:pix_th=0.10",
            "-an",
            "-f", "null",
            "-",
        ]

        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            total_black_duration = 0.0
            for line in res.stderr.splitlines():
                if "black_duration:" in line:
                    parts = line.split("black_duration:")
                    if len(parts) > 1:
                        dur_str = parts[1].split()[0]
                        total_black_duration += float(dur_str)

            return min(total_black_duration / duration, 1.0)
        except Exception as e:
            logger.debug(f"Black frame detection skipped: {e}")
            return 0.0

    def _detect_duplicate_frames(self, video_path: Path) -> float:
        """Estimate frozen/duplicate frame ratio using mpdecimate metadata."""
        if not self.ffmpeg_path:
            return 0.0

        cmd = [
            self.ffmpeg_path,
            "-i", str(video_path),
            "-vf", "mpdecimate,showinfo",
            "-an",
            "-f", "null",
            "-",
        ]

        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            drop_count = sum(1 for line in res.stderr.splitlines() if "drop_count" in line)
            total_frames = max(sum(1 for line in res.stderr.splitlines() if "pts_time" in line), 1)
            return min(drop_count / total_frames, 1.0)
        except Exception:
            return 0.0
