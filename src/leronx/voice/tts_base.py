"""TTS abstraction layer — supports local and cloud engines."""
from __future__ import annotations
import logging, shutil
from pathlib import Path
from abc import ABC, abstractmethod

logger = logging.getLogger("leronx.voice")

class TTSEngine(ABC):
    """Abstract TTS engine. Override synthesize() for custom providers."""
    @abstractmethod
    def synthesize(self, text: str, output_path: Path | None = None) -> Path | None:
        ...

    @classmethod
    def create_default(cls) -> "TTSEngine":
        """Auto-detect best available TTS engine."""
        if shutil.which("espeak"):
            return EspeakTTS()
        if shutil.which("say"):
            return MacSayTTS()
        logger.warning("No TTS engine found. Install espeak or use macOS.")
        return DummyTTS()

class EspeakTTS(TTSEngine):
    def synthesize(self, text: str, output_path: Path | None = None) -> Path | None:
        import subprocess
        out = output_path or Path("/tmp/leronx_tts.wav")
        try:
            subprocess.run(["espeak", "-w", str(out), text[:500]], check=True, capture_output=True)
            return out
        except Exception as e:
            logger.error("espeak failed: %s", e)
            return None

class MacSayTTS(TTSEngine):
    def synthesize(self, text: str, output_path: Path | None = None) -> Path | None:
        import subprocess
        out = output_path or Path("/tmp/leronx_tts.aiff")
        try:
            subprocess.run(["say", "-o", str(out), text[:500]], check=True, capture_output=True)
            return out
        except Exception as e:
            logger.error("macOS say failed: %s", e)
            return None

class DummyTTS(TTSEngine):
    def synthesize(self, text: str, output_path: Path | None = None) -> Path | None:
        logger.info("DummyTTS: would synthesize %d chars", len(text))
        return None
