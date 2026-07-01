"""
Stock footage providers — Pexels, Pixabay API clients.

Register for API keys:
- Pexels: https://www.pexels.com/api/
- Pixabay: https://pixabay.com/api/docs/
"""
from __future__ import annotations
import logging, os, json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional
import urllib.request, urllib.parse

logger = logging.getLogger("leronx.assets")

class StockProvider(ABC):
    """Abstract stock footage provider."""
    @abstractmethod
    def search(self, query: str, per_page: int = 5) -> list[dict[str, Any]]:
        ...
    
class PexelsProvider(StockProvider):
    """Pexels Video API client."""
    BASE_URL = "https://api.pexels.com/videos/search"
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("PEXELS_API_KEY", "")
        if not self.api_key:
            logger.warning("PEXELS_API_KEY not set — Pexels provider disabled")
    def search(self, query: str, per_page: int = 5) -> list[dict]:
        if not self.api_key: return []
        params = urllib.parse.urlencode({"query": query, "per_page": per_page, "orientation": "landscape"})
        req = urllib.request.Request(f"{self.BASE_URL}?{params}", headers={"Authorization": self.api_key})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                return [{"url": v["video_files"][0]["link"], "provider": "pexels", "duration": v.get("duration", 0)} for v in data.get("videos", [])]
        except Exception as e:
            logger.error("Pexels search failed: %s", e)
            return []

class PixabayProvider(StockProvider):
    """Pixabay Video API client."""
    BASE_URL = "https://pixabay.com/api/videos/"
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("PIXABAY_API_KEY", "")
        if not self.api_key:
            logger.warning("PIXABAY_API_KEY not set — Pixabay provider disabled")
    def search(self, query: str, per_page: int = 5) -> list[dict]:
        if not self.api_key: return []
        params = urllib.parse.urlencode({"key": self.api_key, "q": query, "per_page": per_page, "video_type": "all"})
        try:
            with urllib.request.urlopen(f"{self.BASE_URL}?{params}", timeout=10) as resp:
                data = json.loads(resp.read())
                return [{"url": v["videos"]["large"]["url"], "provider": "pixabay", "duration": v.get("duration", 0)} for v in data.get("hits", [])]
        except Exception as e:
            logger.error("Pixabay search failed: %s", e)
            return []
