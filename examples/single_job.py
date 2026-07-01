"""
LeronX Engine — Single Job Example
==================================
Generates a 60-second educational video from a text prompt.

Usage:
    python examples/single_job.py

Requirements:
    pip install leronx-engine
"""
from leronx import Pipeline, PipelineConfig
from leronx.render.config import RenderConfig

def main():
    # Configure pipeline
    config = PipelineConfig(
        gpu_enabled=True,
        codec="h265",
        resolution=(1920, 1080),
        fps=30,
    )

    pipeline = Pipeline(config)

    # Generate video
    print("🎬 Starting LeronX pipeline...")
    result = pipeline.render(
        prompt="The future of artificial intelligence in healthcare",
        tone="professional",
        output_path="./output_healthcare.mp4",
    )

    print(f"✅ Video generated: {result.path}")
    print(f"   Duration: {result.duration}s")
    print(f"   Scenes: {len(result.scenes)}")
    print(f"   Render time: {result.render_time:.1f}s")

if __name__ == "__main__":
    main()
