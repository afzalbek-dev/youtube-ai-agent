"""Unit tests for Metadata Generator."""

from youtube_ai_agent.core.metadata_generator import MetadataGenerator


def test_metadata_generation(mock_settings, sample_scenario):
    """Verify title, tags, and description generation."""
    generator = MetadataGenerator(mock_settings)
    metadata = generator.generate(sample_scenario)

    assert "#Shorts" in metadata.title
    assert len(metadata.title) <= 100
    assert "#Shorts" in metadata.hashtags
    assert len(metadata.tags) >= 5
    assert sample_scenario.hook in metadata.description
    assert metadata.privacy_status == "private"
