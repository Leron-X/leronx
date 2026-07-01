"""
LeronX Engine — AI Video Generation Pipeline
============================================
Modular video generation pipeline: script → scenes → voice → render.

Copyright (c) 2024-2026 LeronX. MIT License.
"""
__version__ = "1.0.0"
__author__ = "LeronX Team"
__license__ = "MIT"

from .pipeline import Pipeline, PipelineResult, PipelineConfig
from .plugins.base import Plugin
from .plugins.registry import PluginRegistry

__all__ = ["Pipeline", "PipelineResult", "PipelineConfig", "Plugin", "PluginRegistry", "__version__"]
