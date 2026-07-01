"""Tests for the main pipeline."""
import pytest
from unittest.mock import patch
from leronx import Pipeline, PipelineConfig

class TestPipeline:
    def test_init_default(self):
        p = Pipeline()
        assert p.config.gpu_enabled is True

    def test_generate_script(self):
        p = Pipeline()
        script = p.generate_script("AI in Healthcare", duration=30)
        assert len(script) > 20

    def test_render_requires_prompt_or_script(self):
        p = Pipeline(PipelineConfig(gpu_enabled=False))
        with pytest.raises(ValueError):
            p.render()

    def test_render_with_mock(self):
        p = Pipeline(PipelineConfig(gpu_enabled=False))
        with patch.object(p, "_render_video") as mock_render, patch.object(p, "_synthesize_voice", return_value=None):
            result = p.render(prompt="Test topic", output_path="/tmp/test_render.mp4")
            assert mock_render.called
            assert len(result.scenes) > 0
