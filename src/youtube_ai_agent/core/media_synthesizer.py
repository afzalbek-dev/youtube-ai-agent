"""Media Synthesizer module for assembling 9:16 vertical YouTube Shorts via FFmpeg."""

import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional
from PIL import Image, ImageDraw, ImageFont

from youtube_ai_agent.config import Settings
from youtube_ai_agent.core.scenario_generator import Scenario, Scene
from youtube_ai_agent.exceptions import MediaSynthesisError

logger = logging.getLogger(__name__)


class MediaSynthesizer:
    """Renders structured video scenarios into 9:16 vertical MP4 video files."""

    def __init__(self, settings: Settings, ffmpeg_bin: Optional[str] = None):
        self.settings = settings
        self.ffmpeg_path = ffmpeg_bin or shutil.which("ffmpeg")
        self.ffprobe_path = shutil.which("ffprobe")

    def check_ffmpeg_available(self) -> bool:
        """Verify that ffmpeg executable is present in PATH."""
        return self.ffmpeg_path is not None and os.path.exists(self.ffmpeg_path)

    def synthesize(self, scenario: Scenario, output_filename: Optional[str] = None) -> Path:
        """Render scenario scenes into an MP4 video file."""
        if not self.check_ffmpeg_available():
            raise MediaSynthesisError(
                "FFmpeg executable not found in PATH. Please install ffmpeg to synthesize videos."
            )

        self.settings.ensure_directories()
        out_name = output_filename or f"short_{scenario.topic.lower().replace(' ', '_')[:24]}.mp4"
        final_video_path = self.settings.output_dir / out_name

        with tempfile.TemporaryDirectory(dir=self.settings.temp_dir) as tmpdir:
            temp_path = Path(tmpdir)
            segment_paths = []

            # Step 1: Render each scene as a visual image and compile to video segment
            for scene in scenario.scenes:
                seg_path = self._render_scene_segment(scene, temp_path)
                segment_paths.append(seg_path)

            # Step 2: Concatenate segments into the final video file
            self._concatenate_segments(segment_paths, final_video_path, temp_path)

        logger.info(f"Successfully synthesized video: {final_video_path}")
        return final_video_path

    def _render_scene_segment(self, scene: Scene, temp_dir: Path) -> Path:
        """Create a 1080x1920 video clip for an individual scene."""
        img_path = temp_dir / f"scene_{scene.scene_number}.png"
        seg_video_path = temp_dir / f"segment_{scene.scene_number}.mp4"

        # Generate 1080x1920 high contrast background with text
        self._create_scene_frame(scene, img_path)

        # Compile image + synthesized tone audio into an MP4 segment
        # Using 440Hz pleasant soft sine wave audio track with anullsrc
        cmd = [
            self.ffmpeg_path,
            "-y",
            "-loop", "1",
            "-i", str(img_path),
            "-f", "lavfi",
            "-i", f"sine=frequency=440:beep_factor=4:sample_rate=44100:duration={scene.duration_seconds}",
            "-t", str(scene.duration_seconds),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-r", str(self.settings.video_fps),
            "-c:a", "aac",
            "-b:a", "128k",
            "-shortest",
            str(seg_video_path),
        ]

        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg segment render failed: {e.stderr}")
            raise MediaSynthesisError(f"Failed to render scene {scene.scene_number}: {e.stderr}")

        return seg_video_path

    def _create_scene_frame(self, scene: Scene, output_path: Path) -> None:
        """Draw a sleek, vertical 9:16 title card with text overlay using Pillow."""
        width = self.settings.video_width
        height = self.settings.video_height

        # Create gradient-like dark tech theme (dark slate to deep navy)
        colors = [
            (15, 23, 42),   # Scene 1: Dark Slate
            (24, 24, 27),   # Scene 2: Zinc
            (17, 24, 39),   # Scene 3: Gray-900
        ]
        bg_color = colors[(scene.scene_number - 1) % len(colors)]
        image = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(image)

        # Header accent bar
        accent_color = (59, 130, 246)  # Electric Blue
        draw.rectangle([(80, 200), (width - 80, 220)], fill=accent_color)

        # Scene badge
        badge_text = f"SCENE 0{scene.scene_number}"
        draw.text((80, 240), badge_text, fill=(148, 163, 184))

        # Text overlay
        overlay_text = scene.text_overlay or f"SCENE {scene.scene_number}"
        draw.text((80, 400), overlay_text, fill=(255, 255, 255))

        # Narration subtitle box
        draw.rectangle([(60, height - 600), (width - 60, height - 250)], fill=(30, 41, 59))
        draw.rectangle([(60, height - 600), (width - 60, height - 250)], outline=(71, 85, 105), width=3)
        draw.text((100, height - 540), scene.narration[:180], fill=(226, 232, 240))

        # Watermark
        draw.text((80, height - 160), "⚡ YouTube AI Agent", fill=(100, 116, 139))

        image.save(output_path, "PNG")

    def _concatenate_segments(self, segments: List[Path], output_path: Path, temp_dir: Path) -> None:
        """Concatenate all video segments into one continuous video file."""
        concat_list_file = temp_dir / "concat_list.txt"
        with open(concat_list_file, "w") as f:
            for seg in segments:
                f.write(f"file '{seg.resolve()}'\n")

        cmd = [
            self.ffmpeg_path,
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list_file),
            "-c", "copy",
            str(output_path),
        ]

        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg concatenation failed: {e.stderr}")
            raise MediaSynthesisError(f"Failed to concatenate segments: {e.stderr}")
