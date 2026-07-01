"""Tests for script generation module."""
import pytest
from leronx.script import ScriptConfig, ScriptGenerator
from leronx.script.config import Tone

class TestScriptConfig:
    def test_default_config(self):
        c = ScriptConfig(topic="AI")
        assert c.tone == Tone.PROFESSIONAL
        assert c.duration == 60
        assert c.max_words == 150

    def test_custom_duration(self):
        c = ScriptConfig(topic="AI", duration=120)
        assert c.max_words == 300

    def test_string_tone_coercion(self):
        c = ScriptConfig(topic="AI", tone="casual")
        assert c.tone == Tone.CASUAL

class TestScriptGenerator:
    def test_generates_script(self):
        gen = ScriptGenerator()
        script = gen.generate(ScriptConfig(topic="Quantum Computing", duration=30))
        assert "[HOOK]" in script
        assert "[BODY]" in script

    def test_no_hook_when_disabled(self):
        gen = ScriptGenerator()
        script = gen.generate(ScriptConfig(topic="AI", include_hooks=False))
        assert "[HOOK]" not in script

    def test_empty_topic_raises(self):
        with pytest.raises(ValueError):
            ScriptGenerator().generate(ScriptConfig(topic=""))
