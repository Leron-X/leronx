"""Plugin registry — manages plugin lifecycle."""
from __future__ import annotations
import logging
from typing import Any, TYPE_CHECKING
from .base import Plugin

if TYPE_CHECKING:
    from ..pipeline import PipelineConfig

logger = logging.getLogger("leronx.plugins")

class PluginRegistry:
    """Registers and runs plugins by stage."""
    def __init__(self):
        self._plugins: list[Plugin] = []

    def register(self, plugin: Plugin) -> None:
        if not isinstance(plugin, Plugin):
            raise TypeError(f"Expected Plugin instance, got {type(plugin)}")
        self._plugins.append(plugin)
        logger.info("Registered plugin: %s (stage=%s)", plugin.name, plugin.stage)

    def unregister(self, name: str) -> None:
        self._plugins = [p for p in self._plugins if p.name != name]

    def run_stage(self, stage: str, context: Any, config: "PipelineConfig") -> Any:
        """Run all plugins for a given stage, sorted by priority."""
        plugins = sorted([p for p in self._plugins if p.stage == stage], key=lambda p: p.priority)
        for plugin in plugins:
            try:
                logger.debug("Running plugin %s at stage %s", plugin.name, stage)
                context = plugin.process(context, config) or context
            except Exception as e:
                logger.error("Plugin %s failed: %s", plugin.name, e)
        return context

    def cleanup_all(self) -> None:
        for plugin in self._plugins:
            try:
                plugin.cleanup()
            except Exception as e:
                logger.warning("Plugin %s cleanup failed: %s", plugin.name, e)

    @property
    def plugins(self) -> list[Plugin]:
        return list(self._plugins)
