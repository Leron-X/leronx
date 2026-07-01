"""Storyboard planner — converts scripts into visual frames."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class StoryboardFrame:
    index: int
    timestamp: float
    description: str
    shot_type: str = "medium"
    camera_move: str = "static"
    duration: float = 3.0
    text_overlay: Optional[str] = None

class StoryboardPlanner:
    SHOTS = {"intro": ("wide", "zoom in"), "body": ("medium", "static"), "detail": ("closeup", "static"), "outro": ("wide", "zoom out")}
    def plan(self, script: str, total_duration: float = 60.0) -> list[StoryboardFrame]:
        scenes = [s.strip() for s in script.split("\n\n") if s.strip()]
        frames, t = [], 0.0
        dur = total_duration / max(len(scenes), 1)
        for i, s in enumerate(scenes):
            shot, cam = self.SHOTS.get("intro" if i == 0 else "outro" if i == len(scenes)-1 else "body")
            frames.append(StoryboardFrame(index=i, timestamp=t, description=s[:200], shot_type=shot, camera_move=cam, duration=dur))
            t += dur
        return frames
