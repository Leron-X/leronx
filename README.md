<div align="center">

# 🎬 LeronX Engine

### Open-Source AI Video Generation Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-47%20passing-brightgreen.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()

**Modular AI video pipeline — script generation → scene planning → rendering → post-production**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Contributing](#-contributing) • [Security](#-security)

</div>

---

## 🧠 Overview

LeronX Engine is the open-source core of [LeronX Pro](https://leronx.org) — an AI-powered video creation platform. This repository contains the **video generation pipeline**: a modular, extensible system that transforms text prompts into fully rendered videos.

> ⚠️ **Note:** This is the engine core, not the full SaaS. Cloud rendering, authentication, billing, and the desktop app are proprietary. See [What's Included](#-whats-included).

## ✨ Features

- **Script Generation** — AI-driven scriptwriting with tone, pacing, and format control
- **Scene Planning** — Automatic scene breakdown with shot composition
- **Asset Management** — Intelligent stock footage matching and generation
- **Voice Synthesis** — Multi-language TTS with emotion control (11 audio languages)
- **Video Rendering** — FFmpeg-based pipeline with transitions, effects, overlays
- **Subtitle Engine** — Auto-aligned, styled subtitles (SRT/ASS/VTT)
- **Plugin System** — Extend any stage of the pipeline
- **GPU Acceleration** — CUDA + Metal support for rendering

## 📦 What's Included

| Module | Status | Description |
|--------|--------|-------------|
| `leronx.script` | ✅ Open Source | Script generation + storyboard planning |
| `leronx.scenes` | ✅ Open Source | Scene graph, transitions, composition |
| `leronx.voice` | ✅ Open Source | TTS abstraction layer (plugin-based) |
| `leronx.render` | ✅ Open Source | FFmpeg pipeline, hardware accel config |
| `leronx.subtitles` | ✅ Open Source | Generation, styling, timing |
| `leronx.assets` | ✅ Open Source | Stock footage API client (Pexels/Pixabay) |
| `leronx.plugins` | ✅ Open Source | Plugin loader + registry |
| `leronx.cloud` | 🔒 Proprietary | Distributed rendering cluster |
| `leronx.auth` | 🔒 Proprietary | Firebase auth + phone verification |
| `leronx.billing` | 🔒 Proprietary | Stripe + credits system |
| `leronx.desktop` | 🔒 Proprietary | Electron/Tauri desktop app |

## 🚀 Quick Start

### Prerequisites

```bash
python >= 3.10
ffmpeg >= 5.0
```

### Installation

```bash
git clone https://github.com/leronx/leronx-engine.git
cd leronx-engine
pip install -e ".[dev]"
```

### Basic Usage

```python
from leronx import Pipeline
from leronx.script import ScriptConfig

# Configure the pipeline
config = ScriptConfig(
    topic="The Future of AI in Healthcare",
    duration=60,  # seconds
    tone="professional",
    language="en",
)

# Create and run pipeline
pipeline = Pipeline(config)
video = pipeline.render(output_path="./output/my_video.mp4")

print(f"✅ Video rendered: {video.path}")
print(f"⏱ Duration: {video.duration}s")
print(f"📂 Scenes: {len(video.scenes)}")
```

### Advanced: Custom Pipeline

```python
from leronx import Pipeline, Plugin
from leronx.scenes import SceneGraph
from leronx.render import RenderConfig

class BrandedOverlay(Plugin):
    """Add LeronX watermark to all videos."""
    
    name = "branded_overlay"
    stage = "post_render"
    
    def process(self, video, config):
        video.add_overlay(
            image="assets/leronx_logo.png",
            position="bottom-right",
            opacity=0.8,
        )
        return video

# Custom pipeline with plugins
pipeline = Pipeline(
    config=RenderConfig(gpu=True, codec="h265"),
    plugins=[BrandedOverlay()],
)

result = pipeline.render(prompt="Explain quantum computing simply")
```

## 🏗 Architecture

```
┌─────────────────────────────────────────────────┐
│                  Pipeline Orchestrator            │
│                                                   │
│  ┌──────┐   ┌────────┐   ┌───────┐   ┌────────┐ │
│  │Script│──▶│Scenes  │──▶│Voice  │──▶│Render  │ │
│  │Gen   │   │Planner │   │Synth  │   │Engine  │ │
│  └──────┘   └────────┘   └───────┘   └────────┘ │
│      │           │           │           │       │
│      ▼           ▼           ▼           ▼       │
│  ┌──────┐   ┌────────┐   ┌───────┐   └────────┐ │
│  │Topics│   │Assets  │   │Subtitle│  │Post-FX │ │
│  │& Tones│  │Match   │   │Engine  │  │& Export│ │
│  └──────┘   └────────┘   └───────┘   └────────┘ │
└─────────────────────────────────────────────────┘
         │                        │
         ▼                        ▼
    ┌─────────┐             ┌──────────┐
    │ Plugins │             │  Output  │
    │ Registry│             │  Formats │
    └─────────┘             └──────────┘
```

### Project Structure

```
leronx-engine/
├── src/leronx/
│   ├── __init__.py          # Pipeline orchestrator
│   ├── pipeline.py          # Core pipeline class
│   ├── script/
│   │   ├── generator.py     # Script generation
│   │   ├── config.py        # Script configuration
│   │   └── storyboard.py    # Visual storyboard planning
│   ├── scenes/
│   │   ├── graph.py         # Scene graph + transitions
│   │   └── composition.py   # Shot composition rules
│   ├── voice/
│   │   ├── tts_base.py      # TTS abstraction
│   │   ├── tts_engines.py   # Provider implementations
│   │   └── emotions.py      # Emotion/prosody control
│   ├── render/
│   professional│   ├── engine.py         # FFmpeg pipeline
│   │   ├── config.py        # Hardware accel config
│   │   └── effects.py       # Transitions, overlays
│   ├── subtitles/
│   │   ├── generator.py     # SRT/ASS/VTT generation
│   │   └── styler.py        # Font, color, positioning
│   ├── assets/
│   │   ├── matcher.py       # Stock footage matcher
│   │   └── providers.py     # Pexels/Pixabay clients
│   └── plugins/
│       ├── base.py          # Plugin interface
│       └── registry.py      # Plugin registry
├── tests/                   # 47 tests (pytest)
├── examples/                # Usage examples
├── docs/                    # Documentation
├── docker/                  # Docker setup
├── pyproject.toml           # Project metadata
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## 🧪 Tests

```bash
pytest tests/ -v --cov=leronx
```

```
========================= test session starts =========================
platform linux -- Python 3.11.5, pytest-7.4.0
collected 47 items

tests/test_script.py .........                                 [ 19%]
tests/test_pipeline.py ........                                [ 36%]
tests/test_scenes.py ..........                                [ 57%]
tests/test_voice.py .......                                    [ 72%]
tests/test_render.py ...........                               [ 96%]
tests/test_plugins.py ..                                       [100%]

---------- coverage: leronx ----------
Name                           Stmts   Miss  Cover
--------------------------------------------------
leronx/__init__.py                12      0   100%
leronx/pipeline.py                45      2    96%
leronx/script/generator.py        38      0   100%
...
TOTAL                            312      8    97%
========================= 47 passed in 2.13s ==========================
```

## 🔌 Plugin Development

```python
from leronx.plugins import Plugin, PluginMeta

class MyPlugin(Plugin, metaclass=PluginMeta):
    name = "my_plugin"
    stage = "pre_render"  # script | scenes | voice | render | post
    priority = 10         # lower runs first

    def process(self, context):
        # Modify the pipeline context
        context.video.add_filter("vintage")
        return context

    def cleanup(self):
        pass
```

## 🐳 Docker

```bash
docker-compose up -d
# API available at http://localhost:8000
```

## 📊 Benchmarks

| GPU | 60s Video | 120s Video | 300s Video |
|-----|-----------|------------|------------|
| RTX 4090 | 45s | 90s | 4min |
| RTX 3080 | 72s | 145s | 6min |
| M2 Max | 58s | 115s | 5min |
| CPU only | 8min | 16min | 40min |

## 🔐 Security

We take security seriously. See [SECURITY.md](SECURITY.md) for responsible disclosure.

## 🤝 Contributing

PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

MIT — see [LICENSE](LICENSE).

## 🔗 Links

- 🌐 [leronx.org](https://leronx.org)
- 📦 [PyPI: leronx-engine](https://pypi.org/project/leronx-engine/)
- 🐛 [Issue Tracker](https://github.com/leronx/leronx-engine/issues)
- 💬 [Discord](https://discord.gg/leronx)

---

<div align="center">

**Built with ❤️ by the LeronX team**

[⬆ Back to top](#-leronx-engine)

</div>
