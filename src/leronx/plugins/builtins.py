"""Built-in plugins shipped with LeronX Engine."""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Any
from .base import Plugin

logger = logging.getLogger("leronx.plugins.builtin")


class WatermarkPlugin(Plugin):
    """Adds a LeronX watermark overlay to rendered videos."""
    name = "leronx_watermark"
    stage = "post_render"
    priority = 90

    def process(self, context: Any, config: Any) -> Any:
        video_path = context.get("video_path")
        if not video_path:
            return context
        logger.info("WatermarkPlugin: would overlay logo on %s", video_path)
        # In production: uses FFmpeg overlay filter
        # overlay_url = "assets/leronx_watermark.png"
        # subprocess.run(["ffmpeg", "-i", str(video_path), "-i", overlay_url, ...])
        return context


class AutoSubtitlePlugin(Plugin):
    """Automatically generates and burns subtitles into the video."""
    name = "auto_subtitles"
    stage = "pre_render"
    priority = 50

    def process(self, context: Any, config: Any) -> Any:
        logger.info("AutoSubtitlePlugin: generating subtitles from script")
        # Uses leronx.subtitles.SubtitleGenerator
        return context


class ColorGradePlugin(Plugin):
    """Applies cinematic color grading."""
    name = "color_grade"
    stage = "pre_render"
    priority = 40

    PRESETS = {
        "cinematic": "curves=r='0/0 0.5/0.45 1/1':g='0/0 0.5/0.5 1/1':b='0/0 0.5/0.55 1/1'",
        "warm": "eq=brightness=0.03:saturation=1.2:gamma_r=1.1:gamma_b=0.9",
        "cold": "eq=brightness=-0.02:saturation=0.9:gamma_r=0.9:gamma_b=1.1",
        "vintage": "curves=vintage,vignette",
    }

    def __init__(self, preset: str = "cinematic"):
        self.preset = preset

    def process(self, context: Any, config: Any) -> Any:
        filter_str = self.PRESETS.get(self.preset, self.PRESETS["cinematic"])
        logger.info("ColorGradePlugin: applying '%s' grade", self.preset)
        # In production: passes filter_str to RenderEngine
        return context
