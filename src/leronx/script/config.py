from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class Tone(str, Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    EDUCATIONAL = "educational"
    DRAMATIC = "dramatic"
    HUMOROUS = "humorous"
    INSPIRATIONAL = "inspirational"

class VideoFormat(str, Enum):
    SHORT = "short"
    LANDSCAPE = "landscape"
    SQUARE = "square"
    PORTRAIT = "portrait"

@dataclass
class ScriptConfig:
    topic: str = ""
    tone: Tone | str = Tone.PROFESSIONAL
    duration: int = 60
    language: str = "en"
    format: VideoFormat | str = VideoFormat.LANDSCAPE
    max_words: int = 0
    include_hooks: bool = True
    include_cta: bool = True
    keywords: list[str] = field(default_factory=list)
    target_audience: Optional[str] = None
    creativity: float = 0.7

    def __post_init__(self):
        if isinstance(self.tone, str):
            self.tone = Tone(self.tone)
        if isinstance(self.format, str):
            self.format = VideoFormat(self.format)
        if self.max_words == 0:
            self.max_words = int((self.duration / 60) * 150)
