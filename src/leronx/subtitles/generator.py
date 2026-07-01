"""Subtitle generator — SRT, ASS, VTT output with timing alignment."""
from __future__ import annotations
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from .styler import SubtitleStyle

logger = logging.getLogger("leronx.subtitles")

@dataclass
class SubtitleEntry:
    index: int
    start: float
    end: float
    text: str

class SubtitleGenerator:
    """Generates subtitles from scripts with timing alignment."""
    def __init__(self, style: SubtitleStyle | None = None):
        self.style = style or SubtitleStyle()

    def generate(self, script: str, total_duration: float, output_path: Path, fmt: str = "srt") -> Path:
        entries = self._parse_to_entries(script, total_duration)
        formatters = {"srt": self._to_srt, "vtt": self._to_vtt, "ass": self._to_ass}
        formatter = formatters.get(fmt, self._to_srt)
        content = formatter(entries)
        output_path = output_path.with_suffix(f".{fmt}")
        output_path.write_text(content, encoding="utf-8")
        logger.info("Subtitles written: %s (%d entries, %s)", output_path, len(entries), fmt)
        return output_path

    def _parse_to_entries(self, script: str, total_duration: float) -> list[SubtitleEntry]:
        import re
        sentences = re.split(r'(?<=[.!?])\s+', script.replace('\n', ' '))
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 2]
        if not sentences: return []
        total_chars = sum(len(s) for s in sentences)
        entries, current_time = [], 0.0
        for i, sentence in enumerate(sentences):
            duration = (len(sentence) / total_chars) * total_duration if total_chars > 0 else 2.0
            entries.append(SubtitleEntry(index=i+1, start=current_time, end=current_time+duration, text=sentence))
            current_time += duration
        return entries

    def _format_time(self, seconds: float, sep: str = ",") -> str:
        h = int(seconds // 3600); m = int((seconds % 3600) // 60)
        s = int(seconds % 60); ms = int((seconds % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"

    def _to_srt(self, entries: list[SubtitleEntry]) -> str:
        return "\n".join(f"{e.index}\n{self._format_time(e.start)} --> {self._format_time(e.end)}\n{e.text}\n" for e in entries)

    def _to_vtt(self, entries: list[SubtitleEntry]) -> str:
        body = "\n".join(f"{self._format_time(e.start, '.')} --> {self._format_time(e.end, '.')}\n{e.text}\n" for e in entries)
        return "WEBVTT\n\n" + body

    def _to_ass(self, entries: list[SubtitleEntry]) -> str:
        header = "[Script Info]\nTitle: LeronX Subtitles\nScriptType: v4.00+\n"
        style_line = f"Style: Default,{self.style.font},{self.style.size},{self.style.color_primary},0,0,0,1,1,0,2,10,10,1\n"
        events = "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
        for e in entries:
            events += f"Dialogue: 0,{self._format_time(e.start, '.')},{self._format_time(e.end, '.')},Default,,0,0,0,,{e.text}\n"
        return header + style_line + events
