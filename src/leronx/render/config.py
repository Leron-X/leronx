"""Render configuration — hardware acceleration, codec, resolution."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class RenderConfig:
    gpu: bool = True
    codec: str = "h265"
    resolution: tuple[int, int] = (1920, 1080)
    fps: int = 30
    bitrate: str = "8M"
    preset: str = "medium"
    hwaccel: str = "auto"  # auto, cuda, videotoolbox, none
    def get_ffmpeg_codec(self) -> str:
        codecs = {"h265": "libx265", "h264": "libx264", "av1": "libaom-av1", "vp9": "libvpx-vp9"}
        return codecs.get(self.codec, "libx264")
    def get_hwaccel_flags(self) -> list[str]:
        if not self.gpu or self.hwaccel == "none": return []
        if self.hwaccel == "cuda": return ["-hwaccel", "cuda", "-hwaccel_output_format", "cuda"]
        if self.hwaccel == "videotoolbox": return ["-hwaccel", "videotoolbox"]
        return []
