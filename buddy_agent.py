import os
import uuid

# ── Language config ────────────────────────────────────────────────────────
_LANG_PREFIXES = {"te": "నమస్కారం! ", "hi": "नमस्ते! ", "en": ""}
_GTTS_CODES    = {"en": "en", "hi": "hi", "te": "te"}

_SYSTEM_PROMPT = (
    "You are Gruha Buddy, an AI interior design expert for Gruha Alankara — "
    "an Indian home design platform. Give practical, concise, helpful answers "
    "about room design, furniture selection, layout tips, color palettes, and "
    "budget planning. Use Indian market prices (INR). Keep replies under 80 words. "
    "Be warm and conversational."
)

# ── Rule-based fallback (used when no Gemini key) ─────────────────────────
_FALLBACK = {
    "sofa":        "Our sofas range from Rs.8,000 to Rs.45,000. The Luxe Comfort Sofa and Urban Corner Sofa are bestsellers. Want me to book one?",
    "table":       "Dining and coffee tables start from Rs.5,000. The Sheesham Dining Table is our most popular pick!",
    "chair":       "Our chair collection ranges from Rs.4,000 to Rs.18,000 — accent chairs, lounge chairs, and dining chairs.",
    "lamp":        "Lighting transforms a room! Pendant lamps, floor lamps, and table lamps from Rs.2,500.",
    "shelf":       "Shelving units from Rs.6,000 to Rs.25,000 — great for storage and display.",
    "price":       "Furniture is priced Rs.5,000–Rs.50,000. We offer EMI and seasonal discounts.",
    "discount":    "10% off on orders above Rs.25,000. Free delivery on orders above Rs.15,000.",
    "delivery":    "Free city delivery on orders above Rs.15,000. Delivery takes 3–7 business days.",
    "color":       "I can suggest color palettes based on your style. Which style interests you — Modern, Scandinavian, or Bohemian?",
    "modern":      "Modern Minimalist uses clean lines, neutral tones, and functional furniture. Perfect for contemporary homes!",
    "scandinavian":"Scandinavian style features light wood, soft tones, and cozy textures — timeless and popular.",
    "budget":      "Share your budget and I'll suggest the best furniture combinations within your range.",
    "book":        "Noted! Our team will contact you within 24 hours to confirm your booking.",
}
_DEFAULT_FALLBACK = (
    "Hello! I am Gruha Buddy, your interior design assistant. "
    "Ask me about furniture, styles, pricing, or room layouts!"
)


def _gemini_reply(user_message: str, language: str) -> str | None:
    """Call Gemini 2.0 Flash. Returns text or None on failure."""
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        lang_hint = ""
        if language == "hi":
            lang_hint = " Reply in Hindi."
        elif language == "te":
            lang_hint = " Reply in Telugu."

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{_SYSTEM_PROMPT}{lang_hint}\n\nUser: {user_message}"
        )
        return response.text.strip()
    except Exception as e:
        print(f"[buddy_agent] Gemini error: {e}")
        return None


def _rule_reply(user_message: str) -> str:
    msg = user_message.lower()
    for keyword, reply in _FALLBACK.items():
        if keyword in msg:
            return reply
    return _DEFAULT_FALLBACK


def _generate_audio(text: str, language: str) -> str | None:
    try:
        from gtts import gTTS
        audio_dir = os.path.join("static", "audio")
        os.makedirs(audio_dir, exist_ok=True)
        filename = f"buddy_{uuid.uuid4().hex[:8]}.mp3"
        filepath = os.path.join(audio_dir, filename)
        lang_code = _GTTS_CODES.get(language, "en")
        gTTS(text=text, lang=lang_code).save(filepath)
        return f"/static/audio/{filename}"
    except Exception:
        return None


def buddy_respond(user_message: str, user_id, language: str = "en") -> dict:
    # 1. Try Gemini AI
    reply = _gemini_reply(user_message, language)

    # 2. Fall back to rule-based
    if not reply:
        reply = _rule_reply(user_message)
        prefix = _LANG_PREFIXES.get(language, "")
        reply  = prefix + reply

    # 3. Generate TTS audio
    audio_url = _generate_audio(reply, language)

    return {"text": reply, "audio_url": audio_url}
