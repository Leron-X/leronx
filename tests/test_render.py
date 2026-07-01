"""Tests for render engine and effects."""
from pathlib import Path
from leronx.render.engine import RenderEngine
from leronx.render.config import RenderConfig
from leronx.render.effects import KenBurns
from leronx.scenes import SceneGraph, Scene

class TestRenderConfig:
    def test_default_codec(self):
        assert RenderConfig().get_ffmpeg_codec() == "libx265"
    def test_hwaccel_none(self):
        assert RenderConfig(gpu=False).get_hwaccel_flags() == []

class TestRenderEngine:
    def test_render_without_ffmpeg(self):
        engine = RenderEngine(gpu=False)
        graph = SceneGraph()
        graph.add_scene(Scene(index=0, start_time=0, end_time=2))
        output = Path("/tmp/test_leronx_render.mp4")
        engine.render(graph, None, output)
        assert output.exists()

class TestEffects:
    def test_ken_burns_filter(self):
        f = KenBurns(duration=5.0).to_ffmpeg_filter(fps=30)
        assert "zoompan" in f
