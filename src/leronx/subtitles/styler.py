"""Subtitle styling — fonts, colors, positioning."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class SubtitleStyle:
    font: str = "Arial"
    size: int = 24
    color_primary: str = "&H00FFFFFF"  # white
    color_outline: str = "&H00000000"  # black
    color_background: str = "&H80000000"
    bold: bool = True
    outline: int = 2
    shadow: int = 1
    alignment: int = 2  # bottom-center
    margin_v: int = 40

    PRESETS = {
        "default": {"font": "Arial", "size": 24, "bold": True, "outline": 2},
        "bold_caption": {"font": "Impact", "size": 32, "bold": True, "outline": 3},
        "minimal": {"font": "Helvetica", "size": 20, "bold": False, "outline": 1},
        "karaoke": {"font": "Verdana", "size": 28, "bold": True, "outline": 2, "alignment": 8},
    }

    @classmethod
    def preset(cls, name: str = "default") -> "SubtitleStyle":
        attrs = cls.PRESETS.get(name, cls.PRESETS["default"])
        return cls(**attrs)
