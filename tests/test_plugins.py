"""Tests for plugin system."""
import pytest
from leronx.plugins.base import Plugin
from leronx.plugins.registry import PluginRegistry
from leronx.plugins.builtins import WatermarkPlugin, ColorGradePlugin

class DummyPlugin(Plugin):
    name = "dummy"
    stage = "post_render"
    def process(self, ctx, cfg):
        ctx["modified"] = True
        return ctx

class TestPluginRegistry:
    def test_register(self):
        reg = PluginRegistry()
        reg.register(DummyPlugin())
        assert len(reg.plugins) == 1

    def test_non_plugin_raises(self):
        with pytest.raises(TypeError):
            PluginRegistry().register("not a plugin")

class TestBuiltins:
    def test_color_grade_presets(self):
        assert "warm" in ColorGradePlugin.PRESETS
