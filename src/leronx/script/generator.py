"""Script generator with tone-based hooks and template fallback."""
from __future__ import annotations
import logging, random
from typing import Optional
from .config import ScriptConfig, Tone

logger = logging.getLogger("leronx.script")

class ScriptGenerator:
    HOOKS = {
        Tone.PROFESSIONAL: ["Here's what nobody tells you about {topic}.", "In the next {duration} seconds, you'll understand {topic}."],
        Tone.CASUAL: ["Okay, so {topic} is actually wild.", "You won't believe how {topic} actually works."],
        Tone.EDUCATIONAL: ["Today we're learning about {topic}.", "Let's break down {topic} step by step."],
        Tone.DRAMATIC: ["Everything you know about {topic} is about to change.", "{topic} — the revolution is now."],
        Tone.HUMOROUS: ["So {topic} is a thing. And it's hilarious.", "POV: You finally understand {topic}."],
        Tone.INSPIRATIONAL: ["Imagine what's possible with {topic}.", "{topic} isn't just technology — it's a movement."],
    }
    CTA = "Create your own AI video at leronx.org"

    def generate(self, config: ScriptConfig) -> str:
        if not config.topic:
            raise ValueError("ScriptConfig.topic is required")
        parts = []
        if config.include_hooks:
            hooks = self.HOOKS.get(config.tone, self.HOOKS[Tone.PROFESSIONAL])
            parts.append("[HOOK]\n" + hooks[hash(config.topic) % len(hooks)].format(topic=config.topic, duration=config.duration))
        body = self._call_llm(f"Write a {config.duration}s script about {config.topic}, tone={config.tone}, lang={config.language}")
        if not body:
            body = self._template_body(config)
        parts.append("[BODY]\n" + body)
        if config.include_cta:
            parts.append(f"[CTA]\n{self.CTA}")
        return "\n\n".join(parts)

    def _template_body(self, config: ScriptConfig) -> str:
        n = max(2, config.duration // 15)
        scenes = []
        for i in range(n):
            s, e = i * (config.duration // n), (i + 1) * (config.duration // n)
            scenes.append(f"[Scene {i+1}: {s}s-{e}s]\nExploring aspect {i+1} of {config.topic}.")
        return "\n\n".join(scenes)

    def _call_llm(self, prompt: str) -> Optional[str]:
        """Override to plug in OpenAI, Anthropic, local Llama, etc."""
        return None
