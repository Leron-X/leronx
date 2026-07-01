"""
Asset Matcher — finds relevant stock footage for scenes.

Uses keyword extraction + provider APIs (Pexels, Pixabay, etc.)
"""
from __future__ import annotations
import logging, re
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger("leronx.assets")

@dataclass 
class AssetMatch:
    scene_index: int
    url: str = ""
    provider: str = "stock"
    relevance: float = 0.0
    keywords: list[str] = field(default_factory=list)

class AssetMatcher:
    """Matches scene descriptions to stock footage."""
    
    STOP_WORDS = {"the", "a", "an", "is", "are", "was", "were", "about", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}

    def extract_keywords(self, text: str, max_keywords: int = 5) -> list[str]:
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        keywords = [w for w in words if w not in self.STOP_WORDS]
        freq = {}
        for w in keywords:
            freq[w] = freq.get(w, 0) + 1
        return [k for k, _ in sorted(freq.items(), key=lambda x: -x[1])[:max_keywords]]

    def match(self, scenes: list[dict], max_per_scene: int = 3) -> list[AssetMatch]:
        """Match assets to scenes (stub — full implementation uses provider APIs)."""
        results = []
        for scene in scenes:
            keywords = self.extract_keywords(scene.get("narration", ""))
            results.append(AssetMatch(
                scene_index=scene["index"],
                keywords=keywords,
                relevance=0.0,  # No provider connected
            ))
        logger.info("Matched %d scenes (stub mode)", len(results))
        return results
