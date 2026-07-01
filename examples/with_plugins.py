"""
LeronX Engine — Plugin Pipeline Example
========================================
Demonstrates custom plugins for the video pipeline.

Usage:
    python examples/with_plugins.py
"""
from leronx import Pipeline, PipelineConfig, Plugin
from leronx.plugins.base import PluginMeta

class VintageFilter(Plugin, metaclass=PluginMeta):
    """Apply a vintage color grade to the video."""
    name = "vintage_filter"
    stage = "pre_render"
    priority = 10

    def process(self, context):
        # Add vintage color grading
        if hasattr(context, "filters"):
            context.filters.append("eq=contrast=1.1:saturation=0.7:brightness=0.05")
        return context

class IntroOverlay(Plugin, metaclass=PluginMeta):
    """Add a branded intro card."""
    name = "intro_overlay"
    stage = "post_render"
    priority = 5

    def process(self, context):
        print("   🎨 Adding intro overlay...")
        return context

def main():
    config = PipelineConfig(
        plugins=[VintageFilter(), IntroOverlay()],
        gpu_enabled=False,
    )

    pipeline = Pipeline(config)
    print("🎬 Pipeline with custom plugins ready")
    print(f"   Registered plugins: {[p.name for p in config.plugins]}")

if __name__ == "__main__":
    main()
