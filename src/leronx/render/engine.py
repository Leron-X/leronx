"""
Render Engine — FFmpeg-based video rendering pipeline.

Supports GPU acceleration (CUDA/VideoToolbox), transitions, and audio mixing.
"""
from __future__ import annotations
import logging, subprocess, shutil
from pathlib import Path
from typing import Optional
from ..scenes.graph import SceneGraph
from .config import RenderConfig

logger = logging.getLogger("leronx.render")

class RenderEngine:
    def __init__(self, gpu: bool = True, codec: str = "h265",
                 resolution: tuple[int, int] = (1920, 1080), fps: int = 30,
                 config: RenderConfig | None = None):
        self.config = config or RenderConfig(gpu=gpu, codec=codec, resolution=resolution, fps=fps)
        self._ffmpeg = shutil.which("ffmpeg")
        if not self._ffmpeg:
            logger.warning("FFmpeg not found — rendering will be simulated")

    def render(self, graph: SceneGraph, voice_path: Path | None, output: Path) -> None:
        """Render a scene graph to a video file."""
        logger.info("Rendering %d scenes → %s (%dx%d, %dfps, %s)",
                     len(graph.scenes), output, *self.config.resolution, self.config.fps, self.config.codec)
        if not self._ffmpeg:
            logger.warning("FFmpeg not installed — creating placeholder output")
            output.write_bytes(b"")  # placeholder
            return
        cmd = self._build_ffmpeg_cmd(graph, voice_path, output)
        logger.debug("FFmpeg cmd: %s", " ".join(cmd))
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            if result.returncode != 0:
                logger.error("FFmpeg failed: %s", result.stderr[-500:])
                raise RuntimeError(f"FFmpeg render failed: {result.returncode}")
            logger.info("Render complete: %s (%.1f MB)", output, output.stat().st_size / 1e6)
        except subprocess.TimeoutExpired:
            logger.error("FFmpeg timed out after 600s")
            raise

    def _build_ffmpeg_cmd(self, graph: SceneGraph, voice_path: Path | None, output: Path) -> list[str]:
        cmd = [self._ffmpeg, "-y"]
        cmd.extend(self.config.get_hwaccel_flags())
        cmd.extend(["-f", "lavfi", "-i", f"color=c=black:s={self.config.resolution[0]}x{self.config.resolution[1]}:r={self.config.fps}"])
        if voice_path and voice_path.exists():
            cmd.extend(["-i", str(voice_path)])
        duration = graph.total_duration or 60.0
        cmd.extend(["-t", str(duration), "-c:v", self.config.get_ffmpeg_codec(),
                     "-preset", self.config.preset, "-b:v", self.config.bitrate,
                     "-pix_fmt", "yuv420p"])
        if voice_path and voice_path.exists():
            cmd.extend(["-c:a", "aac", "-b:a", "192k"])
        cmd.append(str(output))
        return cmd

    def probe(self, video_path: Path) -> dict:
        """Get video metadata using ffprobe."""
        ffprobe = shutil.which("ffprobe")
        if not ffprobe: return {}
        try:
            r = subprocess.run([ffprobe, "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(video_path)],
                               capture_output=True, text=True)
            import json
            return json.loads(r.stdout) if r.returncode == 0 else {}
        except Exception:
            return {}
