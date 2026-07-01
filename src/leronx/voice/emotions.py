"""Emotion/prosody control for TTS engines."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class Emotion(str, Enum):
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    CALM = "calm"
    SERIOUS = "serious"

@dataclass
class VoiceProfile:
    name: str = "narrator"
    emotion: Emotion = Emotion.NEUTRAL
    speed: float = 1.0
    pitch: float = 0.0
    volume: float = 1.0

class EmotionMapper:
    """Maps script tone to TTS emotion parameters."""
    TONE_EMOTION_MAP = {
        "professional": Emotion.SERIOUS, "casual": Emotion.HAPPY,
        "educational": Emotion.CALM, "dramatic": Emotion.EXCITED,
        "humorous": Emotion.HAPPY, "inspirational": Emotion.EXCITED,
    }
    def map_tone(self, tone: str) -> VoiceProfile:
        emotion = self.TONE_EMOTION_MAP.get(tone, Emotion.NEUTRAL)
        speed = {"excited": 1.15, "calm": 0.92, "serious": 0.95}.get(emotion.value, 1.0)
        return VoiceProfile(emotion=emotion, speed=speed)
