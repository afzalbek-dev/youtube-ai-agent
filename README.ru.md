# 🎬 YouTube AI Agent

> **Автономный AI-агент для генерации, контроля качества (QC) и публикации YouTube Shorts.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Supported-green.svg)](https://ffmpeg.org/)
[![Tests](https://img.shields.io/badge/Tests-16%20Passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20Architecture-orange.svg)]()

[Узбекская Версия](README.md) | [English Version](README.en.md)

---

## 📌 Описание проекта

**YouTube AI Agent** — это программный комплекс промышленного уровня (production-ready) для полностью автоматизированного создания, проверки качества и публикации коротких вертикальных видео (YouTube Shorts, 9:16).

Проект решает задачу рутинного видеопроизводства для контент-мейкеров, каналов автоматизации и маркетинговых команд, обеспечивая стабильное качество и защиту конфиденциальных данных.

---

## ✨ Основные возможности

1. **Генерация сценариев (Scenario Generator):**
   - Создание сценариев с высоким удержанием аудитории через Google Gemini 2.5 Flash.
   - Детерминированный **Offline Fallback** режим, работающий без интернета и API ключей.
2. **Медиа-синтез (FFmpeg & Pillow):**
   - Рендеринг вертикального видео Full HD (1080x1920) с частотой 30 кадров/с.
   - Динамическое наложение текста, сцен и синхронизированной аудиодорожки.
   - Корректная обработка отсутствия системного FFmpeg.
3. **Автоматический контроль качества (Quality Inspector):**
   - Детекция черных экранов (фильтр FFmpeg `blackdetect`).
   - Анализ зависших/дублирующихся кадров (`mpdecimate`).
   - Проверка вертикального разрешения 9:16, наличия звука и хронометража.
4. **SEO и генерация метаданных:**
   - Высококликабельные заголовки с тегом `#Shorts`.
   - Полное структурированное описание и ключевые теги для алгоритмов YouTube.
5. **Безопасный шлюз публикации (YouTube Uploader):**
   - По умолчанию включен режим `DRY_RUN=true`, предотвращающий случайные публикации.
   - Публикация возможна только при явном флаге `--force-upload`.
6. **Оповещения в Telegram (Telegram Reporter):**
   - Мгновенные отчеты об успешной генерации с метриками видео.
   - Детальные логи ошибок при сбоях на любом этапе пайплайна.

---

## 🏛 Чистая архитектура (Clean Architecture)

```
src/youtube_ai_agent/
├── config.py             # Настройки Pydantic V2 и .env
├── exceptions.py         # Иерархия исключений
├── pipeline.py           # Оркестратор VideoPipeline
├── cli.py                # Консольный интерфейс Click
└── core/
    ├── scenario_generator.py   # Генератор сценариев и сцен
    ├── media_synthesizer.py    # Сборка медиа через FFmpeg
    ├── quality_inspector.py    # Контроль качества и битых кадров
    ├── metadata_generator.py   # Генерация SEO заголовков и тегов
    ├── youtube_uploader.py     # Безопасный клиент YouTube Data API
    └── telegram_reporter.py    # Telegram бот для уведомлений
```

---

## 🚀 Установка и запуск

### 1. Системные требования
- Python 3.10+
- FFmpeg и FFprobe (`apt install ffmpeg` или `brew install ffmpeg`)

### 2. Установка
```bash
git clone https://github.com/afzalbek-dev/youtube-ai-agent.git
cd youtube-ai-agent
pip install -r requirements.txt
pip install -e .
```

### 3. Настройка переменных окружения
```bash
cp .env.example .env
# Отредактируйте .env при необходимости
```

### 4. Проверка готовности окружения
```bash
youtube-ai-agent status
```

### 5. Создание видео через CLI
```bash
# Запуск пайплайна создания видео
youtube-ai-agent run --topic "Будущее ИИ в 2026 году" --duration 15

# Проверка качества готового файла
youtube-ai-agent inspect output/short_будущее_ии_в_2026_году.mp4
```

---

## 🧪 Тестирование (Pytest)

```bash
pytest -v
```

Все **16 тестов** (юнит и сквозные интеграционные) успешно пройдены:
- Валидация конфигурации: **PASSED**
- Генерация сценариев и оффлайн режим: **PASSED**
- Обработка ошибок FFmpeg: **PASSED**
- Проверка соотношения сторон и черных кадров: **PASSED**
- Режим Dry-Run для YouTube: **PASSED**
- Моки Telegram уведомлений: **PASSED**
- Полный сквозной цикл пайплайна: **PASSED**

---

## 🐳 Запуск в Docker

```bash
docker compose build
docker compose run --rm youtube-ai-agent run --topic "Технологии будущего"
```

---

## 🔒 Безопасность

- Ключи API и конфиденциальные данные не хранятся в репозитории (`.gitignore`).
- Реальная публикация отключена по умолчанию.

---

## 📄 Лицензия

MIT License. Автор: [Afzalbek](https://github.com/afzalbek-dev).
