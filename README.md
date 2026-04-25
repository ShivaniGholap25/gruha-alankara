# Gruha Alankara
AI-powered interior design assistant with AR-inspired room capture, smart recommendations, and voice-enabled buddy support.

## Prerequisites
- Python 3.8+

## Setup
1. `python -m venv venv`
2. `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. `pip install -r requirements.txt`
4. `python run.py`
5. Open `http://localhost:5000`
6. Go to `http://localhost:5000/seed-db` to populate furniture data

## Features
- AR camera room capture workflow
- AI-powered interior design recommendations
- Buddy agent for conversational furniture help and booking
- Multilingual voice responses (English, Telugu, Hindi)

## Tech Stack
| Layer | Technology |
|---|---|
| Backend | Flask, Flask-SQLAlchemy |
| Database | SQLite |
| AI Vision | Hugging Face Transformers (BLIP image captioning) |
| AI Text | Hugging Face text-generation models |
| Agent | LangChain + custom tools |
| Voice | gTTS |
| Frontend | Jinja2 templates, vanilla JavaScript, CSS |
| Testing | Python unittest + Flask test client |
