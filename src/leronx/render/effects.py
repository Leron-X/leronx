"""Visual effects — transitions, overlays, Ken Burns effect."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class Transition:
    type: str = "fade"  # fade, dissolve, wipe, slide, zoom
    duration: float = 0.5

@dataclass
class Overlay:
    image_path: str = ""
    position: str = "bottom-right"  # top-left, center, bottom-right, etc.
    opacity: float = 1.0
    scale: float = 1.0

@dataclass
class KenBurns:
    """Ken Burns effect for static images."""
    zoom_start: float = 1.0
    zoom_end: float = 1.15
    pan_x: float = 0.0
    pan_y: float = 0.0
    duration: float = 5.0

    def to_ffmpeg_filter(self, fps: int = 30) -> str:
        frames = int(self.duration * fps)
        return (f"zoompan=z='min(zoom+0.0015,{self.zoom_end})':"
                f"d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080")

class EffectsPipeline:
    """Chain of visual effects applied during rendering."""
    def __init__(self):
        self._effects: list = []
    def add_transition(self, transition: Transition) -> None:
        self._effects.append(("transition", transition))
    def add_overlay(self, overlay: Overlay) -> None:
        self._effects.append(("overlay", overlay))
    def add_ken_burns(self, kb: KenBurns) -> None:
        self._effects.append(("ken_burns", kb))
    @property
    def effects(self) -> list:
        return self._effects
