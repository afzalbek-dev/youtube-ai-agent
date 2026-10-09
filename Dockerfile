# Multi-stage lightweight Dockerfile for YouTube AI Agent
FROM python:3.12-slim-bookworm AS base

# Install system dependencies: FFmpeg and essential tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and config
COPY pyproject.toml .
COPY src/ ./src/
COPY tests/ ./tests/
COPY .env.example .

RUN pip install --no-cache-dir -e .

# Create output and temp directories
RUN mkdir -p /app/output /app/temp && chmod -R 777 /app/output /app/temp

# Non-root user for security
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["youtube-ai-agent"]
CMD ["--help"]
