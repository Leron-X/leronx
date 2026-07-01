"""Composition planner — breaks scripts into scenes with shot types."""
from __future__ import annotations
import logging, re
from .graph import SceneGraph, Scene

logger = logging.getLogger("leronx.scenes")

class CompositionPlanner:
    """Plans scene composition from a script."""
    def plan(self, script: str, target_duration: int = 60) -> SceneGraph:
        blocks = self._parse_script(script)
        n = max(len(blocks), 1)
        scene_dur = target_duration / n
        graph = SceneGraph()
        for i, block in enumerate(blocks):
            start = i * scene_dur
            scene = Scene(
                index=i, start_time=start, end_time=start + scene_dur,
                narration=block.strip()[:500],
                shot_type=self._pick_shot(i, n),
                transition="cut" if i == 0 else self._pick_transition(i),
            )
            graph.add_scene(scene)
        logger.info("Planned %d scenes, total %.1fs", len(graph.scenes), graph.total_duration)
        return graph

    def _parse_script(self, script: str) -> list[str]:
        parts = re.split(r'\[Scene \d+[^\]]*\]|\n\n', script)
        return [p.strip() for p in parts if p.strip() and not p.startswith('[')]

    def _pick_shot(self, idx: int, total: int) -> str:
        if idx == 0: return "wide"
        if idx == total - 1: return "wide"
        if idx % 3 == 0: return "closeup"
        return "medium"

    def _pick_transition(self, idx: int) -> str:
        transitions = ["cut", "fade", "dissolve", "wipe"]
        return transitions[idx % len(transitions)]
