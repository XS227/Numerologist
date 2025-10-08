# Numerologist 🔢✨

Numerologist is an AI-driven web platform for **numerology analysis**, **character profiling**, and **life-path forecasting** — blending data science with spiritual symbolism.

It is developed and maintained by [Arshian Visionary & Intelligence](https://biiaab.ir) as part of the "Setaei Intelligence" ecosystem.

---

## 🚀 Features
- Dynamic numerology calculations (Pythagorean & Chaldean)
- Personality mapping (1–9 archetypes + master numbers)
- AI-based text interpretation of results
- Birthdate → Life Path visual charts
- Name Analyzer (vowel/consonant balance)
- Localization support (English / Norwegian / Persian)
- API ready for integrations with other Arshian projects

---

## 🧩 Tech Stack
| Layer | Technology |
|-------|-------------|
| Frontend | Python Flask / FastAPI (planned React UI) |
| Backend | Django (REST API) |
| Database | PostgreSQL / SQLite (dev) |
| Hosting | Codex + FTP Deployment (numerologist.setaei.com) |
| Version Control | GitHub |
| Dev Tools | Figma, VSCode, Docker (future), GitHub Actions |

---

## 🌍 Deployment
Current live subdomain:
> https://numerologist.setaei.com

---

## 🧪 Status
🟢 **MVP Phase** — Core numerology engine and UI under development.  
🧭 **Next:** Integrate dynamic charts and AI explanations (OpenAI API / local LLM).

---

## 📖 Documentation
- [Setup Guide](docs/Setup_Guide.md)
- [Numerology Engine](docs/Numerology_Engine.md)
- [API Reference](docs/API_Reference.md)
- [Architecture Overview](docs/Architecture_Overview.md)
- [Contributors & Credits](docs/Contributors_and_Credits.md)

---

# 🛠️ Setup Guide

## Requirements
- Python 3.11+
- pip / virtualenv
- Git

## Installation
```bash
git clone https://github.com/XS227/Numerologist.git
cd Numerologist
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

If you see `ModuleNotFoundError: No module named 'django'` when running management
commands, double-check that the dependency installation finished successfully.
Corporate or sandboxed environments may block outbound PyPI traffic; in that
case download the wheels from a networked machine and install them via
`pip install --no-index --find-links <wheel-directory> -r requirements.txt`.
