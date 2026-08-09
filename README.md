# 🎬 YouTube AI Agent

An AI-powered automation platform for **generating, processing, scheduling, and publishing short-form YouTube videos** with minimal manual work.

> Portfolio & project documentation repository. Source code is not published here.

## 🚀 Project Overview

YouTube AI Agent is designed as an end-to-end content automation pipeline for YouTube Shorts. It can analyze channel performance, choose content ideas, generate prompts, create visuals, produce short videos, validate output quality, and publish automatically on a schedule.

## 🧠 AI Content Workflow

1. Analyze channel performance and recent content
2. Select a topic or content idea
3. Generate the scenario and visual prompt with Gemini
4. Create a vertical 9:16 image
5. Generate an AI video from the image
6. Process the video with FFmpeg
7. Add CTA/branding elements
8. Validate duration, format and quality
9. Publish automatically to YouTube

## ✨ Main Features

- Automated topic selection
- AI-generated scripts and prompts
- AI image generation
- Image-to-video generation
- Automatic video processing
- YouTube Shorts optimization
- Scheduled publishing
- Hashtag and metadata generation
- Duplicate-content prevention
- Failed-stage retry logic
- Telegram status notifications
- Content history tracking

## 🎥 Video Pipeline

Designed for short vertical content:

- 9:16 aspect ratio
- Full HD vertical output
- Short-form video duration
- Audio presence checks
- Black-frame detection
- Duplicate detection
- Watermark checks
- CTA integration
- Final MP4 optimization

## 🔁 Reliability & Automation

- Stage-based workflow
- Retry only failed stages
- Duplicate prevention through content hashing
- Idempotent publishing logic
- Scheduled task execution
- Distributed-lock-ready architecture
- Publishing history and state tracking

## 📊 Analytics Integration

- YouTube channel performance analysis
- Content trend detection
- Topic prioritization
- Performance-aware future content planning
- Video publishing history

## 🧰 Technology Stack

**AI:** Gemini API, image-generation models, video-generation models  
**Backend:** Python  
**Media:** FFmpeg  
**YouTube:** YouTube Data API, YouTube Analytics API  
**Automation:** Schedulers, background jobs  
**Notifications:** Telegram Bot API  
**Infrastructure:** Linux, Docker-ready architecture

## 🛡️ Quality Control

The system can validate generated content before publishing, including:

- Expected video duration
- Correct 9:16 resolution
- Audio availability
- No blank or black output
- No accidental duplicates
- Valid media encoding
- Successful upload state

## 🎯 Project Goal

The goal is to build a scalable AI content engine that reduces repetitive video-production work and allows creators to maintain a consistent YouTube Shorts publishing schedule.

## 📩 Developer

Developed as part of **Afzalbek's AI & automation portfolio**.

Telegram: `@Obunachi786`

---

© 2026 Afzalbek — Portfolio Project
