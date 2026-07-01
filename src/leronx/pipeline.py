"""
Pipeline Orchestrator — core video generation flow.
"""
from __future__ import annotations
import logging, time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from .plugins.base import Plugin
from .plugins.registry import PluginRegistry
from .script.config import ScriptConfig
from .script.generator import ScriptGenerator
from .scenes.graph import SceneGraph
from .scenes.composition import CompositionPlanner

logger = logging.getLogger("leronx.pipeline")

@dataclass
class PipelineConfig:
    script: ScriptConfig = field(default_factory=ScriptConfig)
    gpu_enabled: bool = True
    codec: str = "h265"
    output_format: str = "mp4"
    resolution: tuple[int, int] = (1920, 1080)
    fps: int = 30
    plugins: list[Plugin] = field(default_factory=list)
    work_dir: Path = Path("/tmp/leronx")

@dataclass
class PipelineResult:
    path: Path
    duration: float
    scenes: list[dict[str, Any]]
    script: str
    voice_track: Optional[Path] = None
    subtitle_file: Optional[Path] = None
    render_time: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

class Pipeline:
    def __init__(self, config: PipelineConfig | ScriptConfig | None = None):
        if config is None:
            config = PipelineConfig()
        elif isinstance(config, ScriptConfig):
            config = PipelineConfig(script=config)
        self.config = config
        self.registry = PluginRegistry()
        for plugin in config.plugins:
            self.registry.register(plugin)
        self._script_gen = ScriptGenerator()
        self._scene_planner = CompositionPlanner()
        logger.info("Pipeline initialized (gpu=%s, codec=%s, plugins=%d)", config.gpu_enabled, config.codec, len(config.plugins))

    def generate_script(self, prompt: str, *, tone: str = "professional", duration: int = 60, language: str = "en") -> str:
        config = ScriptConfig(topic=prompt, tone=tone, duration=duration, language=language)
        return self._script_gen.generate(config)

    def plan_scenes(self, script: str) -> SceneGraph:
        return self._scene_planner.plan(script)

    def render(self, prompt: Optional[str] = None, *, script: Optional[str] = None, output_path: str | Path = "./output.mp4") -> PipelineResult:
        if prompt is None and script is None:
            raise ValueError("Either 'prompt' or 'script' must be provided")
        start_time = time.monotonic()
        if script is None:
            script = self.generate_script(prompt)
        script = self.registry.run_stage("pre_scene", script, self.config)
        graph = self.plan_scenes(script)
        graph = self.registry.run_stage("pre_voice", graph, self.config)
        voice_path = self._synthesize_voice(script)
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        self._render_video(graph, voice_path, output)
        render_time = time.monotonic() - start_time
        post_ctx = {"video_path": output, "graph": graph, "config": self.config}
        self.registry.run_stage("post_render", post_ctx, self.config)
        return PipelineResult(path=output, duration=graph.total_duration, scenes=[s.to_dict() for s in graph.scenes], script=script, voice_track=voice_path, render_time=render_time)

    def _synthesize_voice(self, script: str) -> Path | None:
        try:
            from .voice.tts_base import TTSEngine
            return TTSEngine.create_default().synthesize(script)
        except Exception as e:
            logger.warning("Voice synthesis skipped: %s", e)
            return None

    def _render_video(self, graph: SceneGraph, voice_path: Path | None, output: Path) -> None:
        from .render.engine import RenderEngine
        engine = RenderEngine(gpu=self.config.gpu_enabled, codec=self.config.codec, resolution=self.config.resolution, fps=self.config.fps)
        engine.render(graph, voice_path, output)
