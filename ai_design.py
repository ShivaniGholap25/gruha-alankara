import os
import base64
import json
import random


# ── Fallback design data (used when Claude is unavailable) ─────────────────
_FALLBACK = {
    "Modern Minimalist": {
        "furniture": ["Low-profile sofa", "Glass coffee table", "Geometric shelving", "Platform bed", "Accent chair"],
        "colors": ["#FFFFFF", "#000000", "#808080", "#F5F5F5"],
        "materials": ["Glass", "Steel", "Concrete", "Light wood"],
    },
    "Scandinavian": {
        "furniture": ["Platform Bed", "Dresser", "Nightstand", "Wooden Desk", "Accent Chair"],
        "colors": ["#F5F0E8", "#2C5F2E", "#D4A373", "#FEFAE0"],
        "materials": ["Pine wood", "Linen", "Wool", "Ceramic"],
    },
    "Industrial": {
        "furniture": ["Leather Sofa", "Metal Bookshelf", "Concrete Coffee Table", "Iron Floor Lamp", "TV Stand"],
        "colors": ["#2E2E2E", "#5A5A5A", "#8C7B75", "#B0A8A0"],
        "materials": ["Raw steel", "Exposed brick", "Concrete", "Distressed wood"],
    },
    "Bohemian": {
        "furniture": ["Rattan Chair", "Patterned Ottoman", "Low Coffee Table", "Hanging Lamp", "Open Shelf"],
        "colors": ["#E76F51", "#2A9D8F", "#E9C46A", "#F4A261"],
        "materials": ["Rattan", "Jute", "Cotton weave", "Carved wood"],
    },
    "Traditional": {
        "furniture": ["Tufted Sofa", "Carved Side Table", "Classic Armchair", "Wood Console", "Display Cabinet"],
        "colors": ["#7A4E2D", "#C9B79C", "#8B0000", "#F5E6CC"],
        "materials": ["Teak wood", "Brass", "Velvet", "Marble"],
    },
    "Contemporary": {
        "furniture": ["Modular Sofa", "Accent Chair", "Smart TV Unit", "Glass Center Table", "Statement Lamp"],
        "colors": ["#D9D9D9", "#4A4E69", "#9A8C98", "#F2E9E4"],
        "materials": ["Tempered glass", "Matte metal", "Engineered wood", "Textured fabric"],
    },
}

NOT_A_ROOM = "NOT_A_ROOM"

_VISION_PROMPT = """You are an interior design AI. Analyse this room photo.
If this is NOT a room interior (e.g. street, landscape, person, food, car), respond with exactly:
NOT_A_ROOM

If it IS a room interior, respond with JSON only (no markdown, no code fences):
{"room_type": string, "style": string, "detected_colors": ["#hex1","#hex2","#hex3"], "furniture_suggestions": [{"name": string, "reason": string, "price_inr": integer}, ...3-5 items], "layout_tip": string}

Prices must reflect real Indian market rates (sofa ₹15000-₹80000, chair ₹4000-₹18000, table ₹8000-₹35000, lamp ₹2500-₹12000, shelf ₹6000-₹25000)."""


def analyze_room_with_vision(image_path: str) -> dict | str:
    """
    Call Claude claude-sonnet-4-20250514 with vision to analyse a room image.
    Returns parsed dict on success, NOT_A_ROOM string if not a room,
    or None if Claude is unavailable (caller falls back to PIL analysis).
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return None  # no key → caller uses PIL fallback

    try:
        import anthropic

        with open(image_path, "rb") as f:
            raw = f.read()
        b64 = base64.standard_b64encode(raw).decode("utf-8")

        # Detect media type from file header
        if raw[:3] == b"\xff\xd8\xff":
            media_type = "image/jpeg"
        elif raw[:8] == b"\x89PNG\r\n\x1a\n":
            media_type = "image/png"
        elif raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
            media_type = "image/webp"
        else:
            media_type = "image/jpeg"

        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": b64,
                            },
                        },
                        {"type": "text", "text": _VISION_PROMPT},
                    ],
                }
            ],
        )

        text = message.content[0].text.strip()

        if text == NOT_A_ROOM:
            return NOT_A_ROOM

        # Strip accidental markdown fences
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()

        return json.loads(text)

    except Exception:
        return None  # any error → PIL fallback


def get_fallback_design(style_theme: str) -> dict:
    data = _FALLBACK.get(style_theme, _FALLBACK["Modern Minimalist"])
    return {
        "furniture": data["furniture"],
        "color_scheme": data["colors"],
        "materials": data["materials"],
        "placement_tips": f"Arrange furniture to maximise space flow for {style_theme} style.",
    }


def generate_design(image_path: str, style_theme: str) -> dict:
    return get_fallback_design(style_theme)
