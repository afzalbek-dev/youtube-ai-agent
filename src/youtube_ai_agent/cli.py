"""Command Line Interface for YouTube AI Agent."""

import logging
import sys
from pathlib import Path
import click

from youtube_ai_agent.config import get_settings
from youtube_ai_agent.pipeline import VideoPipeline
from youtube_ai_agent.core.quality_inspector import QualityInspector
from youtube_ai_agent.core.media_synthesizer import MediaSynthesizer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("youtube_ai_agent")


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """⚡ YouTube AI Agent — Autonomous YouTube Shorts Production CLI."""
    pass


@cli.command()
def status():
    """Inspect environment readiness, FFmpeg, and API connectivity."""
    settings = get_settings()
    synth = MediaSynthesizer(settings)
    
    click.echo("\n🔍 YouTube AI Agent Environment Readiness:")
    click.echo("=" * 50)
    
    # FFmpeg status
    ffmpeg_ok = synth.check_ffmpeg_available()
    ffmpeg_icon = "✅" if ffmpeg_ok else "❌"
    click.echo(f"{ffmpeg_icon} FFmpeg Available: {synth.ffmpeg_path or 'NOT FOUND'}")
    
    # AI Provider status
    gemini_ok = bool(settings.gemini_api_key)
    gemini_icon = "✅" if gemini_ok else "⚠️"
    gemini_info = "Configured" if gemini_ok else "Missing (Offline Fallback will be used)"
    click.echo(f"{gemini_icon} Gemini API Key: {gemini_info}")

    # Telegram status
    tg_ok = bool(settings.telegram_bot_token and settings.telegram_chat_id)
    tg_icon = "✅" if tg_ok else "ℹ️"
    tg_info = "Enabled" if tg_ok else "Disabled / Local logs only"
    click.echo(f"{tg_icon} Telegram Reporter: {tg_info}")

    # YouTube Upload safety status
    yt_icon = "🛡️" if not settings.youtube_upload_enabled else "⚠️"
    click.echo(f"{yt_icon} YouTube Uploading: {'DISABLED (Dry-Run)' if not settings.youtube_upload_enabled else 'ENABLED'}")
    click.echo(f"📁 Output Directory: {settings.output_dir.resolve()}")
    click.echo("=" * 50 + "\n")


@cli.command()
@click.option("--topic", "-t", required=True, help="Topic for the YouTube Shorts video.")
@click.option("--duration", "-d", default=15.0, type=float, help="Target duration in seconds.")
@click.option("--output", "-o", default=None, help="Output MP4 file name.")
@click.option("--force-upload", is_flag=True, default=False, help="Explicitly confirm real YouTube upload.")
def run(topic: str, duration: float, output: str, force_upload: bool):
    """Generate, synthesize, quality check, and prepare a short video."""
    settings = get_settings()
    pipeline = VideoPipeline(settings)

    click.echo(f"\n🚀 Launching video generation pipeline for: '{topic}'...")
    try:
        result = pipeline.run(
            topic=topic,
            target_duration=duration,
            output_filename=output,
            force_upload=force_upload,
        )
        click.echo("\n🎉 Pipeline Execution Completed Successfully!")
        click.echo(f"• Video Path: {result.video_path}")
        click.echo(f"• Title: {result.metadata.title}")
        click.echo(f"• Duration: {result.quality_report.duration_seconds:.1f}s")
        click.echo(f"• Quality QC: {'PASSED' if result.quality_report.is_valid else 'FAILED'}")
        click.echo(f"• Upload Status: {result.upload_result.status} (Dry-Run: {result.upload_result.is_dry_run})")
    except Exception as e:
        click.secho(f"\n❌ Pipeline failed: {e}", fg="red", err=True)
        sys.exit(1)


@cli.command()
@click.argument("video_path", type=click.Path(exists=True, path_type=Path))
def inspect(video_path: Path):
    """Run Quality Inspection QC checks on an existing video file."""
    settings = get_settings()
    inspector = QualityInspector(settings)

    click.echo(f"\n🔬 Inspecting video: {video_path}...")
    report = inspector.inspect(video_path)

    click.echo(f"• Valid 9:16 Aspect: {'YES' if report.width < report.height else 'NO'} ({report.width}x{report.height})")
    click.echo(f"• Duration: {report.duration_seconds:.2f}s")
    click.echo(f"• Audio Stream: {'PRESENT' if report.has_audio_track else 'MISSING'}")
    click.echo(f"• Black Frame Ratio: {report.black_frame_ratio:.2%}")
    click.echo(f"• Duplicate Frame Ratio: {report.duplicate_frame_ratio:.2%}")

    if report.is_valid:
        click.secho("\n✅ Video passed all quality requirements!", fg="green")
    else:
        click.secho("\n❌ Video failed QC checks:", fg="red")
        for fail in report.failures:
            click.echo(f"  - {fail}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
