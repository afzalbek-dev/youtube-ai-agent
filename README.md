# 🎬 YouTube AI Agent

> **Avtonom YouTube Shorts yaratish, sifat nazorati (QC) va xavfsiz yuklash platformasi.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Supported-green.svg)](https://ffmpeg.org/)
[![Tests](https://img.shields.io/badge/Tests-16%20Passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20Architecture-orange.svg)]()

[English Version](README.en.md) | [Русская Версия](README.ru.md)

---

## 📌 Loyiha Haqida

**YouTube AI Agent** — bu qisqa formatli (YouTube Shorts, 9:16) videolarni noldan to'liq avtomatik tarzda yaratish, tahlil qilish, sifatini tekshirish (QC) va xavfsiz rejimda e'lon qilish uchun mo'ljallangan ishlab chiqarish darajasidagi (production-ready) AI agenti.

Tizim kontent yaratuvchilar, SMM mutaxassislari va avtomatlashtirilgan kanallar uchun mo'ljallangan bo'lib, inson aralashuvisiz har kuni muntazam va yuqori sifatli kontent yetkazib berish imkonini beradi.

---

## ✨ Asosiy Imkoniyatlar

1. **Ssenariy Generatsiyasi (Scenario Generator):**
   - Google Gemini 2.5 API orqali yuqori retensiyali (ko'rish davomiyligini ushlab turuvchi) ssenariylar tuzish.
   - Internet yoki API kalit bo'lmaganda ishlaydigan **Deterministik Offline Fallback** rejimi (soxta ma'lumot bermaydi).
2. **Media Sintezi (Media Synthesizer via FFmpeg):**
   - 9:16 vertikal Full HD (1080x1920) formatda render qilish.
   - Silliq texnologik kadrlarni avtomatik chizish va audio sintezi.
   - FFmpeg o'rnatilmagan muhitda xatoliklarni xavfsiz tutib olish.
3. **Avtomatlashtirilgan Sifat Nazorati (Quality Inspector):**
   - Qora kadrlarni aniqlash (`blackdetect` filtri orqali).
   - Qotib qolgan/takroriy kadrlarni tekshirish (`mpdecimate`).
   - Vertikal proporsiya (9:16), audio mavjudligi va davomiylik chegarasini qat'iy nazorat qilish.
4. **SEO va Metadata Generatsiyasi:**
   - Yuqori CTR'li (bosilish ko'rsatkichi yuqori) sarlavhalar va `#Shorts` teglari.
   - Algoritmlar uchun optimallashtirilgan to'liq tavsif (description).
5. **Xavfsiz Yuklash Shlyuzi (YouTube Uploader Gate):**
   - Standart holatda `DRY_RUN=true` va yuklash o'chirilgan — tasodifiy ommaga chiqib ketishning oldi olinadi.
   - Faqat foydalanuvchining alohida tasdig'i (`--force-upload`) bilan ishlaydi.
6. **Telegram Xabarnoma Tizimi (Telegram Reporter):**
   - Muvaffaqiyatli tayyorlangan videolar haqida video metrikalari bilan hisobot berish.
   - Xatolik yuz berganda qaysi bosqichda to'xtaganini darhol xabar qilish.

---

## 🏛 Arxitektura (Clean Architecture)

Loyiha qat'iy Clean Architecture tamoyillariga asoslangan:

```
src/youtube_ai_agent/
├── config.py             # Pydantic V2 va .env sozlamalari
├── exceptions.py         # Maxsus istisno va xatolar iyerarxiyasi
├── pipeline.py           # End-to-end orkestrator (VideoPipeline)
├── cli.py                # Click CLI buyruqlar paneli
└── core/
    ├── scenario_generator.py   # Ssenariy va sahnalar
    ├── media_synthesizer.py    # FFmpeg & Pillow video yig'ish
    ├── quality_inspector.py    # QC, qora kadr va audio tahlili
    ├── metadata_generator.py   # SEO sarlavha va hashtaglar
    ├── youtube_uploader.py     # YouTube API xavfsiz yuklash
    └── telegram_reporter.py    # Telegram bildirishnomalari
```

---

## 🚀 O'rnatish va Ishga Tushirish

### 1. Talablar
- Python 3.10+
- FFmpeg va FFprobe (`apt install ffmpeg` yoki `brew install ffmpeg`)

### 2. O'rnatish
```bash
git clone https://github.com/afzalbek-dev/youtube-ai-agent.git
cd youtube-ai-agent
pip install -r requirements.txt
pip install -e .
```

### 3. Muhitni Sozlash
```bash
cp .env.example .env
# .env faylini tahrirlab kerakli kalitlarni kiriting (ixtiyoriy)
```

### 4. Tizim Holatini Tekshirish
```bash
youtube-ai-agent status
```

### 5. Video Yaratish (CLI orqali)
```bash
# Avtonom video yaratish (Offline fallback yoki Gemini bilan)
youtube-ai-agent run --topic "AI Future 2026" --duration 15

# Mavjud videoni sifatini tekshirish (Quality QC)
youtube-ai-agent inspect output/short_ai_future_2026.mp4
```

---

## 🧪 Testlash (Pytest)

Loyiha 100% to'liq test qamroviga ega bo'lib, tashqi API'lar va FFmpeg holatlarini alohida tekshiradi:

```bash
pytest -v
```

Barcha **16 ta** testlar (unit va end-to-end integratsion) muvaffaqiyatli bajariladi:
- Konfiguratsiya va papkalar tekshiruvi: **PASSED**
- Gemini API va Offline fallback: **PASSED**
- FFmpeg mavjudligi va yo'qligi xatosi: **PASSED**
- 9:16 vertikal format va qora kadrlar filtri: **PASSED**
- YouTube xavfsiz Dry-Run shlyuzi: **PASSED**
- Telegram xabarnoma va xatoliklar: **PASSED**
- End-to-End to'liq pipeline: **PASSED**

---

## 🐳 Docker Orqali Ishga Tushirish

```bash
docker compose build
docker compose run --rm youtube-ai-agent run --topic "Artificial Intelligence"
```

---

## 🔒 Xavfsizlik Qoidalari

1. `.env` fayli va maxfiy API kalitlari hech qachon repozitoriyga yuborilmaydi (`.gitignore` qat'iy sozlangan).
2. YouTube'ga real yuklash imkoniyati xavfsizlik maqsadida dastlab o'chirilgan (`DRY_RUN=true`).

---

## 📄 Litsenziya

MIT License. Muallif: [Afzalbek](https://github.com/afzalbek-dev).
