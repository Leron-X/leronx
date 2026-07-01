# LeronX Engine — Docker Image
FROM python:3.12-slim

LABEL maintainer="LeronX Team"
LABEL description="Open-Source AI Video Generation Pipeline"

# System dependencies (FFmpeg + codecs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Python package
WORKDIR /app
COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -e .

# Source code
COPY src/ ./src/
COPY tests/ ./tests/
COPY examples/ ./examples/

# Default config
ENV LERONX_GPU=false
ENV LERONX_CODEC=h265

ENTRYPOINT ["python", "-m", "leronx"]
