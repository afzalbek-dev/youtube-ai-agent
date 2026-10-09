"""End-to-End Orchestrator Pipeline for YouTube AI Agent."""

import logging
from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from youtube_ai_agent.config import Settings, get_settings
from youtube_ai_agent.core.scenario_generator import Scenario, ScenarioGenerator
from youtube_ai_agent.core.metadata_generator import MetadataGenerator, VideoMetadata
from youtube_ai_agent.core.media_synthesizer import MediaSynthesizer
from youtube_ai_agent.core.quality_inspector import QualityInspector, QualityReport
from youtube_ai_agent.core.youtube_uploader import YouTubeUploader, UploadResult
from youtube_ai_agent.core.telegram_reporter import TelegramReporter
from youtube_ai_agent.exceptions import PipelineError, QualityCheckFailedError

logger = logging.getLogger(__name__)


class PipelineResult(BaseModel):
    """Aggregate result from executing the full video pipeline."""
    topic: str
    scenario: Scenario
    metadata: VideoMetadata
    video_path: str
    quality_report: QualityReport
    upload_result: UploadResult
    success: bool
    summary_message: str


class VideoPipeline:
    """Coordinates scenario generation, media synthesis, QA inspection, and publishing."""

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self.scenario_gen = ScenarioGenerator(self.settings)
        self.metadata_gen = MetadataGenerator(self.settings)
        self.media_synth = MediaSynthesizer(self.settings)
        self.quality_insp = QualityInspector(self.settings)
        self.uploader = YouTubeUploader(self.settings)
        self.reporter = TelegramReporter(self.settings)

    def run(
        self,
        topic: str,
        target_duration: Optional[float] = None,
        output_filename: Optional[str] = None,
        force_upload: bool = False,
    ) -> PipelineResult:
        """Execute full video creation lifecycle."""
        logger.info(f"Starting YouTube AI Agent pipeline for topic: '{topic}'")
        self.settings.ensure_directories()

        try:
            # Stage 1: Generate Scenario
            logger.info("Stage 1/5: Generating scenario...")
            scenario = self.scenario_gen.generate(topic, target_duration=target_duration)

            # Stage 2: Generate Metadata
            logger.info("Stage 2/5: Generating metadata...")
            metadata = self.metadata_gen.generate(scenario)

            # Stage 3: Synthesize Media
            logger.info("Stage 3/5: Synthesizing media via FFmpeg...")
            video_path = self.media_synth.synthesize(scenario, output_filename=output_filename)

            # Stage 4: Quality Inspection
            logger.info("Stage 4/5: Running quality inspection...")
            quality_report = self.quality_insp.inspect(video_path)
            if not quality_report.is_valid:
                error_msg = f"Video failed QC criteria: {', '.join(quality_report.failures)}"
                self.reporter.report_failure(topic, "Quality Inspection", error_msg)
                raise QualityCheckFailedError(error_msg, failures=quality_report.failures)

            # Stage 5: Upload / Dry-Run Gate
            logger.info("Stage 5/5: Processing upload gate...")
            upload_result = self.uploader.upload(video_path, metadata, force_upload=force_upload)

            # Success notification
            self.reporter.report_success(
                topic=topic,
                video_path=str(video_path),
                duration=quality_report.duration_seconds,
                title=metadata.title,
            )

            summary = (
                f"Successfully produced '{metadata.title}' ({quality_report.duration_seconds:.1f}s). "
                f"Status: {upload_result.status}."
            )
            logger.info(f"Pipeline finished: {summary}")

            return PipelineResult(
                topic=topic,
                scenario=scenario,
                metadata=metadata,
                video_path=str(video_path),
                quality_report=quality_report,
                upload_result=upload_result,
                success=True,
                summary_message=summary,
            )

        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            self.reporter.report_failure(topic, "Pipeline Execution", str(e))
            raise
