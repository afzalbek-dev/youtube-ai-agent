# 🎬 YouTube AI Agent

> **Autonomous AI-Powered YouTube Shorts Generation, Quality Control, and Publishing Engine.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Supported-green.svg)](https://ffmpeg.org/)
[![Tests](https://img.shields.io/badge/Tests-16%20Passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20Architecture-orange.svg)]()

[O'zbekcha Versiya](README.md) | [Русская Версия](README.ru.md)

---

## 📌 Project Overview

**YouTube AI Agent** is a production-grade, autonomous software agent designed to generate, synthesize, quality-check, and safely publish high-retention short-form videos (YouTube Shorts, 9:16 vertical format).

Built for creators, automation channels, and marketing teams, this system eliminates repetitive production workflows while maintaining strict broadcast quality standards and zero-leak credential security.

---

## ✨ Key Features

1. **AI Scenario Generation:**
   - Script generation with Google Gemini 2.5 Flash for high-retention storytelling (hook, body, payoff, CTA).
   - Deterministic, high-quality **Offline Fallback Mode** when API keys are omitted or unavailable.
2. **Media Synthesis (FFmpeg & Pillow):**
   - High-definition 9:16 vertical output (1080x1920) optimized for YouTube Shorts.
   - Dynamic slide and typography synthesis with synchronized audio tracks.
   - Graceful error recovery when system media tools are missing.
3. **Automated Quality Inspection (QC):**
   - Black frame detection via FFmpeg `blackdetect` filter.
   - Frozen / duplicate frame ratio checks via `mpdecimate`.
   - Strict vertical aspect ratio, audio presence, and duration validation before publishing.
4. **Metadata & SEO Generation:**
   - High-CTR mobile-optimized titles with `#Shorts` tags.
   - Keyword-rich descriptions and tag arrays tailored to YouTube recommendation algorithms.
5. **Safety-First Upload Gate:**
   - Default `DRY_RUN=true` and disabled network uploads to prevent accidental public releases.
   - Explicit confirmation flag required for production publishing.
6. **Telegram Lifecycle Reporting:**
   - Instant progress alerts upon successful generation with full video metrics.
   - Immediate failure alerts with diagnostic details if any pipeline stage fails.

---

## 🏛 Clean Architecture

```
src/youtube_ai_agent/
├── config.py             # Pydantic V2 and .env configuration
├── exceptions.py         # Custom pipeline exception hierarchy
├── pipeline.py           # End-to-end orchestrator (VideoPipeline)
├── cli.py                # Click CLI interface
└── core/
    ├── scenario_generator.py   # Script & scene generator
    ├── media_synthesizer.py    # FFmpeg media assembler
    ├── quality_inspector.py    # Automated QC & black frame detection
    ├── metadata_generator.py   # SEO titles & tags
    ├── youtube_uploader.py     # Safe YouTube API client
    └── telegram_reporter.py    # Telegram alerts & logs
```

---

## 🚀 Installation & Quick Start

### 1. Requirements
- Python 3.10+
- FFmpeg and FFprobe (`sudo apt install ffmpeg` or `brew install ffmpeg`)

### 2. Setup
```bash
git clone https://github.com/afzalbek-dev/youtube-ai-agent.git
cd youtube-ai-agent
pip install -r requirements.txt
pip install -e .
```

### 3. Configuration
```bash
cp .env.example .env
# Edit .env with your optional API keys
```

### 4. Check Environment Readiness
```bash
youtube-ai-agent status
```

### 5. Generate Video via CLI
```bash
# Run autonomous video pipeline
youtube-ai-agent run --topic "AI Revolution in 2026" --duration 15

# Inspect video quality
youtube-ai-agent inspect output/short_ai_revolution_in_2026.mp4
```

---

## 🧪 Testing Suite (Pytest)

The project includes an exhaustive Pytest test suite covering unit logic and end-to-end workflows:

```bash
pytest -v
```

All **16 tests** pass with verified zero mock pollution:
- Configuration validation: **PASSED**
- Scenario generator & Offline fallback: **PASSED**
- FFmpeg availability and error handling: **PASSED**
- Quality control & aspect ratio checks: **PASSED**
- Dry-run upload safety gate: **PASSED**
- Telegram reporting mocks: **PASSED**
- Full end-to-end pipeline execution: **PASSED**

---

## 🐳 Docker Deployment

```bash
docker compose build
docker compose run --rm youtube-ai-agent run --topic "Autonomous AI Agents"
```

---

## 🔒 Security & Secrets Management

- Secrets and tokens are loaded strictly via environment variables (`.env`).
- Real credentials and media artifacts are excluded via `.gitignore`.
- Automated uploads require explicit user confirmation.

---

## 📄 License

MIT License. Developed by [Afzalbek](https://github.com/afzalbek-dev).
