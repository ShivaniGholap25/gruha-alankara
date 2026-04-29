import os
import json
import base64
from PIL import Image, ImageStat
from google import genai
from google.genai import types

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


# ─────────────────────────────────────────────
# Public entry points
# ─────────────────────────────────────────────

def analyze_room_image(image_path: str) -> dict:
    if GEMINI_API_KEY:
        try:
            return _gemini_analyze(image_path)
        except Exception as e:
            print(f"[ai_design] Gemini error, using PIL fallback: {e}")
    return _pil_analyze(image_path)


def generate_design(style_theme: str, budget: int = 50000, room_type: str = "Living Room") -> dict:
    if GEMINI_API_KEY:
        try:
            return _gemini_design(style_theme, budget, room_type)
        except Exception as e:
            print(f"[ai_design] Gemini design error, using rule fallback: {e}")
    return _rule_based_design(style_theme, budget, room_type)


# ─────────────────────────────────────────────
# Gemini vision analysis
# ─────────────────────────────────────────────

def _gemini_analyze(image_path: str) -> dict:
    import PIL.Image
    img = PIL.Image.open(image_path)
    prompt = """You are an interior design analyst. Look at this image carefully.

FIRST: Is this a room interior such as bedroom, living room, kitchen, bathroom, office, or dining room?

If it is NOT a room interior, respond with only this exact JSON and nothing else:
{"not_a_room": true}

If it IS a room interior, respond with only this JSON and nothing else, no markdown, no explanation:
{"room_type": "<detected room type>","dimensions": {"width": <estimated feet as number>, "length": <estimated feet as number>, "height": <estimated feet as number>, "area": <sq ft as number>},"lighting": {"quality": "<natural or artificial or mixed>", "brightness": <0 to 100 as number>, "description": "<one sentence>"},"colors": ["<hex1>", "<hex2>", "<hex3>", "<hex4>", "<hex5>"],"features": {"complexity": "<simple or moderate or complex>", "notable": "<key design feature in 5 words>"},"furniture_visible": ["<item1>", "<item2>"],"style_hint": "<modern or traditional or bohemian or scandinavian or industrial or contemporary>"}"""

    response = _client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[img, prompt]
    )
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()
    data = json.loads(text)
    if data.get("not_a_room"):
        return {
            "error": "not_a_room",
            "message": "Please upload a photo of a room (bedroom, living room, kitchen, etc.)"
        }
    return data


# ─────────────────────────────────────────────
# Gemini design generation
# ─────────────────────────────────────────────

def _gemini_design(style_theme: str, budget: int, room_type: str) -> dict:
    prompt = f"""You are an expert Indian interior designer. Create a complete design plan.
Style: {style_theme}
Budget: Rs.{budget:,}
Room type: {room_type}

Respond with only this JSON, no markdown, no explanation:
{{"style_theme": "{style_theme}","description": "<2 sentence style description>","furniture": [{{"name": "<item name>", "quantity": 1, "priority": "essential", "price_inr": <realistic Indian market price as number>}},{{"name": "<item name>", "quantity": 1, "priority": "essential", "price_inr": <price as number>}},{{"name": "<item name>", "quantity": 1, "priority": "recommended", "price_inr": <price as number>}},{{"name": "<item name>", "quantity": 1, "priority": "optional", "price_inr": <price as number>}}],"colors": ["<hex1>", "<hex2>", "<hex3>", "<hex4>"],"materials": ["<material1>", "<material2>", "<material3>"],"layout_tips": ["<tip1>", "<tip2>", "<tip3>"],"ai_story": "<3 sentences about how this design feels and why it suits the room>","space_utilization": <number between 60 and 95>,"budget_breakdown": [{{"category": "Furniture", "percent": 45, "amount": {int(budget*0.45)}}},{{"category": "Flooring", "percent": 20, "amount": {int(budget*0.20)}}},{{"category": "Lighting", "percent": 15, "amount": {int(budget*0.15)}}},{{"category": "Decor", "percent": 12, "amount": {int(budget*0.12)}}},{{"category": "Labour", "percent": 8, "amount": {int(budget*0.08)}}}],"savings_tips": ["<tip1>", "<tip2>", "<tip3>"]}}"""

    response = _client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


# ─────────────────────────────────────────────
# PIL fallback — used when no API key present
# ─────────────────────────────────────────────

def _pil_analyze(image_path: str) -> dict:
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    stat = ImageStat.Stat(img)
    brightness = int(sum(stat.mean[:3]) / 3)
    quality = "natural" if brightness > 120 else "artificial" if brightness < 80 else "mixed"
    small = img.resize((50, 50))
    quantized = small.quantize(5)
    palette = quantized.getpalette()[:15]
    colors = ["#{:02x}{:02x}{:02x}".format(palette[i], palette[i+1], palette[i+2]) for i in range(0, 15, 3)]
    return {
        "room_type": "living_room",
        "dimensions": {
            "width": round(w * 0.05, 1),
            "length": round(h * 0.05, 1),
            "height": 9.0,
            "area": round(w * 0.05 * h * 0.05, 1)
        },
        "lighting": {"quality": quality, "brightness": brightness, "description": "Estimated via image analysis"},
        "colors": colors,
        "features": {"complexity": "moderate", "notable": "Estimated via image analysis"},
        "furniture_visible": [],
        "style_hint": "modern"
    }


# ─────────────────────────────────────────────
# Rule-based design fallback
# ─────────────────────────────────────────────

STYLE_DATA = {
    "Modern Minimalist": {
        "description": "Clean lines and a neutral palette create a serene, clutter-free environment.",
        "furniture": [
            {"name": "Low-profile sofa 3-seater", "quantity": 1, "priority": "essential", "price_inr": 28000},
            {"name": "Tempered glass coffee table", "quantity": 1, "priority": "essential", "price_inr": 12000},
            {"name": "Floating TV unit", "quantity": 1, "priority": "essential", "price_inr": 18000},
            {"name": "Accent armchair", "quantity": 1, "priority": "recommended", "price_inr": 9500},
        ],
        "colors": ["#F5F5F0", "#2C2C2C", "#C0A882", "#7D9B8A"],
        "materials": ["Engineered wood", "Tempered glass", "Microfiber fabric"],
    },
    "Scandinavian": {
        "description": "Functional warmth with light wood tones and cozy textiles.",
        "furniture": [
            {"name": "Solid pine wood sofa", "quantity": 1, "priority": "essential", "price_inr": 32000},
            {"name": "Round birch coffee table", "quantity": 1, "priority": "essential", "price_inr": 9500},
            {"name": "Knitted throw and cushions set", "quantity": 1, "priority": "essential", "price_inr": 3500},
            {"name": "Pendant lamp linen shade", "quantity": 1, "priority": "recommended", "price_inr": 6800},
        ],
        "colors": ["#FAFAF7", "#D4C4A0", "#8BA8B0", "#4A5568"],
        "materials": ["Light pine wood", "Linen fabric", "Wool"],
    },
    "Industrial": {
        "description": "Raw textures, exposed materials, and utilitarian design with urban character.",
        "furniture": [
            {"name": "Leather sectional sofa", "quantity": 1, "priority": "essential", "price_inr": 45000},
            {"name": "Metal-wood coffee table", "quantity": 1, "priority": "essential", "price_inr": 14500},
            {"name": "Industrial bookshelf metal", "quantity": 1, "priority": "recommended", "price_inr": 22000},
            {"name": "Edison bulb pendant 3-pack", "quantity": 1, "priority": "recommended", "price_inr": 4500},
        ],
        "colors": ["#3D3D3D", "#8B7355", "#C0C0C0", "#1A1A1A"],
        "materials": ["Reclaimed wood", "Wrought iron", "Aged leather"],
    },
    "Bohemian": {
        "description": "Layered textiles, global patterns, and eclectic art create vibrant soulfulness.",
        "furniture": [
            {"name": "Low-floor sofa with bolsters", "quantity": 1, "priority": "essential", "price_inr": 22000},
            {"name": "Jute macrame wall art set", "quantity": 1, "priority": "essential", "price_inr": 5500},
            {"name": "Carved wood side table", "quantity": 1, "priority": "recommended", "price_inr": 8000},
            {"name": "Patterned area rug 6x9 ft", "quantity": 1, "priority": "essential", "price_inr": 12000},
        ],
        "colors": ["#C4955A", "#8B4513", "#6B8E6B", "#9B59B6"],
        "materials": ["Jute", "Hand-block printed cotton", "Teak wood"],
    },
    "Traditional": {
        "description": "Rich wood tones, classic upholstery, and timeless Indian craftsmanship.",
        "furniture": [
            {"name": "Sheesham wood sofa set 3+1+1", "quantity": 1, "priority": "essential", "price_inr": 55000},
            {"name": "Teak centre table with carving", "quantity": 1, "priority": "essential", "price_inr": 28000},
            {"name": "Brass floor lamp", "quantity": 1, "priority": "recommended", "price_inr": 8500},
            {"name": "Silk brocade curtains pair", "quantity": 1, "priority": "recommended", "price_inr": 7500},
        ],
        "colors": ["#8B4513", "#DAA520", "#F5DEB3", "#2F4F4F"],
        "materials": ["Sheesham wood", "Teak", "Silk upholstery"],
    },
    "Contemporary": {
        "description": "Current trends blended with comfort, bold accents on neutral bases.",
        "furniture": [
            {"name": "Sectional sofa L-shape", "quantity": 1, "priority": "essential", "price_inr": 42000},
            {"name": "Sintered stone coffee table", "quantity": 1, "priority": "essential", "price_inr": 18500},
            {"name": "Modular wall shelving", "quantity": 1, "priority": "recommended", "price_inr": 15000},
            {"name": "Arc floor lamp", "quantity": 1, "priority": "recommended", "price_inr": 9500},
        ],
        "colors": ["#F0EDE8", "#2C3E50", "#E74C3C", "#BDC3C7"],
        "materials": ["Sintered stone", "Velvet fabric", "Brushed steel"],
    },
}

ROOM_TIPS = {
    "living_room": ["Place sofa facing natural light", "Use a large area rug to anchor seating", "Keep TV at eye level"],
    "bedroom":     ["Position bed on the longest wall", "Add blackout curtains for better sleep", "Use under-bed storage"],
    "kitchen":     ["Maximise vertical storage with tall units", "Install under-cabinet LED strips", "Use a kitchen island if space allows"],
    "bathroom":    ["Use light tiles to visually enlarge", "Install a rain shower for luxury feel", "Add floating vanity for storage"],
    "office":      ["Place desk perpendicular to window", "Use cable management trays", "Add a plant for productivity"],
    "dining_room": ["Choose a table 30 inches shorter than room", "Hang chandelier 30 to 36 inches above table", "Mirror on one wall doubles visual space"],
}


def _rule_based_design(style_theme: str, budget: int, room_type: str) -> dict:
    style = STYLE_DATA.get(style_theme, STYLE_DATA["Modern Minimalist"])
    tips  = ROOM_TIPS.get(room_type.lower().replace(" ", "_"), ROOM_TIPS["living_room"])
    return {
        "style_theme": style_theme,
        "description": style["description"],
        "furniture": style["furniture"],
        "colors": style["colors"],
        "materials": style["materials"],
        "layout_tips": tips,
        "ai_story": (
            f"Your {room_type.replace('_', ' ')} deserves the warmth of {style_theme} design. "
            f"With a budget of Rs.{budget:,}, you can create a space that feels curated and personal. "
            f"Every piece selected here balances aesthetics with the practical needs of Indian living."
        ),
        "space_utilization": 78,
        "budget_breakdown": [
            {"category": "Furniture", "percent": 45, "amount": int(budget * 0.45)},
            {"category": "Flooring",  "percent": 20, "amount": int(budget * 0.20)},
            {"category": "Lighting",  "percent": 15, "amount": int(budget * 0.15)},
            {"category": "Decor",     "percent": 12, "amount": int(budget * 0.12)},
            {"category": "Labour",    "percent": 8,  "amount": int(budget * 0.08)},
        ],
        "savings_tips": [
            "Buy furniture during Diwali or Navratri sales for 20 to 40 percent off",
            "Consider second-hand sheesham wood from OLX for excellent quality",
            "DIY decor items like macrame and painted pots save Rs.5000 to Rs.10000",
        ],
    }
