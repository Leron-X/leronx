"""Tests for TTS and emotion mapping."""
from leronx.voice.tts_base import TTSEngine, DummyTTS
from leronx.voice.emotions import Emotion, EmotionMapper

class TestEmotionMapper:
    def test_professional_maps_to_serious(self):
        assert EmotionMapper().map_tone("professional").emotion == Emotion.SERIOUS

class TestTTSEngine:
    def test_dummy_returns_none(self):
        assert DummyTTS().synthesize("test") is None
