"""Custom exceptions for the YouTube AI Agent pipeline."""

class PipelineError(Exception):
    """Base exception for all pipeline errors."""
    pass

class ConfigurationError(PipelineError):
    """Raised when environment or runtime configuration is invalid."""
    pass

class ScenarioGenerationError(PipelineError):
    """Raised when scenario generation fails."""
    pass

class MediaSynthesisError(PipelineError):
    """Raised when FFmpeg or media processing fails."""
    pass

class QualityCheckFailedError(PipelineError):
    """Raised when generated media does not satisfy quality criteria."""
    def __init__(self, message: str, failures: list[str] | None = None):
        super().__init__(message)
        self.failures = failures or []

class UploadError(PipelineError):
    """Raised when YouTube upload fails."""
    pass

class NotificationError(PipelineError):
    """Raised when Telegram or status notification fails."""
    pass
