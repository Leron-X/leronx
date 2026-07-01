"""Scene graph — structured representation of video scenes and transitions."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass
class Scene:
    index: int
    start_time: float
    end_time: float
    narration: str = ""
    shot_type: str = "medium"
    transition: str = "cut"
    assets: list[str] = field(default_factory=list)
    text_overlay: Optional[str] = None

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    def to_dict(self) -> dict[str, Any]:
        return {"index": self.index, "start": self.start_time, "end": self.end_time,
                "duration": self.duration, "shot": self.shot_type, "transition": self.transition,
                "narration": self.narration[:100], "text_overlay": self.text_overlay}

@dataclass
class SceneGraph:
    scenes: list[Scene] = field(default_factory=list)
    total_duration: float = 0.0
    def add_scene(self, scene: Scene) -> None:
        self.scenes.append(scene)
        self.total_duration = max(self.total_duration, scene.end_time)
    def __len__(self) -> int:
        return len(self.scenes)
    def __iter__(self):
        return iter(self.scenes)
