"""Plugin base class — extend any stage of the pipeline."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class Plugin(ABC):
    """
    Base class for all pipeline plugins.
    
    Override the process() method to modify pipeline behavior at any stage.
    
    Stages:
        - pre_scene: modify script before scene planning
        - pre_voice: modify scene graph before voice synthesis
        - pre_render: modify context before rendering
        - post_render: modify output after rendering
    """
    name: str = "base_plugin"
    stage: str = "post_render"
    priority: int = 10  # lower runs first

    @abstractmethod
    def process(self, context: Any, config: Any) -> Any:
        """Process and optionally modify the pipeline context."""
        ...

    def cleanup(self) -> None:
        """Optional cleanup after pipeline completes."""
        pass

    def __repr__(self) -> str:
        return f"<Plugin:{self.name} stage={self.stage} priority={self.priority}>"
