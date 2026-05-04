import os
import uuid
import random


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


def get_smart_response(msg):
    """Comprehensive rule-based responses covering all interior design topics."""

    # Greetings
    if any(w in msg for w in ["hello", "hi", "hey", "namaste", "hii", "howdy"]):
        return random.choice([
            "Hello! I am Gruha Buddy, your personal interior design assistant. How can I help you transform your space today?",
            "Hi there! Ready to design your dream home? Ask me about furniture, styles, or room layouts!",
            "Hey! Welcome to Gruha Alankara. I can help you with furniture selection, design styles, budgeting, and much more!"
        ])

    # How are you
    if any(w in msg for w in ["how are you", "how r you", "whats up", "what's up"]):
        return "I am doing great and ready to help you design beautiful spaces! What room would you like to transform today?"

    # Furniture general
    if any(w in msg for w in ["furniture", "furnitures", "tell me about furniture"]):
        return """Our furniture collection includes:
🛋️ SOFAS: Starting from Rs.8,000 - Perfect for living rooms
🪑 CHAIRS: Accent chairs, lounge chairs from Rs.4,000
🪞 TABLES: Dining tables, coffee tables from Rs.5,000
💡 LAMPS: Floor lamps, pendant lights from Rs.2,500
📚 SHELVES: Wall shelves, bookshelves from Rs.6,000
Visit our Furniture page to browse and book! Which category interests you?"""

    # Sofa
    if any(w in msg for w in ["sofa", "couch", "settee"]):
        return """🛋️ Our Sofa Collection:
1. Luxe Comfort Sofa - Rs.18,500 (3-seater fabric sofa, perfect for family rooms)
2. Urban Corner Sofa - Rs.32,000 (L-shaped, ideal for modern living rooms)

Tips for choosing a sofa:
- Measure your room before buying
- Consider fabric vs leather based on lifestyle
- Check if it fits through your door!
Would you like to book one of these?"""

    # Chair
    if any(w in msg for w in ["chair", "seating", "seat"]):
        return """🪑 Our Chair Collection:
1. Nordic Accent Chair - Rs.7,800 (Soft upholstery, Scandinavian style)
2. Ergo Lounge Chair - Rs.14,200 (Curved design with wooden legs)

Perfect for reading corners or as accent pieces!
Which style appeals to you - Modern or Classic?"""

    # Table
    if any(w in msg for w in ["table", "dining table", "coffee table", "desk"]):
        return """🪞 Our Table Collection:
1. Sheesham Dining Table - Rs.27,500 (Solid wood, seats 6)
2. Minimal Coffee Table - Rs.9,500 (Compact with storage shelf)

Pro tip: For dining tables, allow 90cm clearance on all sides for comfortable movement.
Interested in either of these?"""

    # Lamp / Lighting
    if any(w in msg for w in ["lamp", "light", "lighting", "bulb"]):
        return """💡 Lighting transforms any room! Our collection:
1. Pendant Glow Lamp - Rs.5,600 (Warm white, ideal for dining)
2. Tripod Floor Lamp - Rs.11,200 (Great for reading corners)

Lighting Tips:
- Use warm light (3000K) for bedrooms and living rooms
- Use cool light (5000K) for kitchens and offices
- Layer lighting: overhead + accent + task lights
What room are you lighting up?"""

    # Shelf
    if any(w in msg for w in ["shelf", "shelves", "bookshelf", "storage"]):
        return """📚 Our Storage Solutions:
1. Modular Wall Shelf - Rs.8,600 (Floating shelves, modern look)
2. Industrial Book Shelf - Rs.22,800 (Metal and wood, statement piece)

Storage Tips:
- Floating shelves make rooms look bigger
- Group items in odd numbers for visual appeal
- Mix books with decorative items
Which style matches your room?"""

    # Price / Cost / Budget
    if any(w in msg for w in ["price", "cost", "budget", "cheap", "expensive", "affordable", "rate"]):
        return """💰 Gruha Alankara Price Range:
🛋️ Sofas: Rs.8,000 - Rs.45,000
🪑 Chairs: Rs.4,000 - Rs.18,000
🪞 Tables: Rs.5,000 - Rs.35,000
💡 Lamps: Rs.2,500 - Rs.15,000
📚 Shelves: Rs.6,000 - Rs.25,000

Budget Tips:
✅ EMI options on orders above Rs.20,000
✅ Free delivery on orders above Rs.15,000
✅ 10% discount on orders above Rs.25,000
What is your budget range?"""

    # Discount / Offer / Sale
    if any(w in msg for w in ["discount", "offer", "sale", "deal", "coupon"]):
        return """🎉 Current Offers:
- 10% OFF on orders above Rs.25,000
- FREE delivery on orders above Rs.15,000
- Buy 2 chairs, get 10% off
- Festival season sale: Up to 30% off on selected items

Tip: Mix high-end statement pieces with budget-friendly basics for the best value!"""

    # Booking / Order
    if any(w in msg for w in ["book", "order", "buy", "purchase", "want to buy"]):
        return """📦 How to Book Furniture:
1. Go to Furniture page (top navigation)
2. Browse our collection
3. Click Book Now on your chosen item
4. Confirm your booking
5. Our team will contact you within 24 hours

Delivery time: 3-7 business days
We also offer installation service!
Which item would you like to book?"""

    # Delivery / Shipping
    if any(w in msg for w in ["delivery", "shipping", "when", "days", "time"]):
        return """🚚 Delivery Information:
- Standard delivery: 3-7 business days
- Express delivery: 1-2 days (extra charge)
- FREE delivery on orders above Rs.15,000
- Installation service available
- We deliver across major Indian cities

Our team will call you before delivery to confirm the time slot!"""

    # Design styles general
    if any(w in msg for w in ["modern", "minimalist", "style", "theme", "design style"]):
        return """🎨 Popular Design Styles in Gruha Alankara:
1. Modern Minimalist - Clean lines, neutral colors
2. Scandinavian - Natural materials, cozy textures
3. Industrial - Raw materials, urban character
4. Bohemian - Eclectic, colorful, expressive
5. Traditional - Classic, timeless elegance
6. Contemporary - Trend-forward, sleek

Use our Style Quiz to find your perfect style!
Which style interests you most?"""

    # Scandinavian
    if any(w in msg for w in ["scandinavian", "nordic", "scandi"]):
        return """🌿 Scandinavian Style Guide:
Key Features:
- Light wood tones (pine, birch)
- Neutral colors (white, beige, gray)
- Cozy textures (wool, linen)
- Minimalist furniture with organic shapes
- Lots of natural light

Perfect for: Bedrooms, Living rooms
Recommended furniture: Platform Bed, Wooden Desk, Accent Chair"""

    # Industrial style
    if any(w in msg for w in ["industrial", "loft", "urban"]):
        return """🔧 Industrial Style Guide:
Key Features:
- Exposed brick and metal
- Dark, moody color palette
- Raw, unfinished textures
- Edison bulb lighting
- Leather and steel furniture

Perfect for: Living rooms, Home offices
Recommended: Leather Sofa, Metal Bookshelf, Tripod Floor Lamp"""

    # Color
    if any(w in msg for w in ["color", "colour", "paint", "palette", "colors"]):
        return """🎨 Color Guide for Interiors:
Living Room: Warm neutrals (beige, cream, warm gray)
Bedroom: Soft blues, greens, lavender (calming)
Kitchen: White, light gray, yellow (energizing)
Office: Blue, green (focus and productivity)

The 60-30-10 Rule:
- 60% dominant color (walls)
- 30% secondary color (furniture)
- 10% accent color (decor)

Our Design Studio has 8 color themes to choose from!"""

    # Room analysis
    if any(w in msg for w in ["analyze", "analysis", "room analysis", "scan", "measure"]):
        return """📸 Room Analysis Feature:
Upload a photo of your room and our AI will detect:
✅ Room dimensions (width, length, height)
✅ Lighting quality and brightness
✅ Dominant color palette
✅ Room complexity and features
✅ Recommended design styles

Go to Analyze Room page to try it!
For best results use a well-lit, wide-angle photo."""

    # AR Camera
    if any(w in msg for w in ["ar", "augmented reality", "camera", "visualize", "3d"]):
        return """📷 AR Camera Feature:
See furniture in YOUR room before buying!

How to use:
1. Go to Live AR Camera page
2. Allow camera permission
3. Point at your room
4. Select furniture to place
5. See how it looks in real time!

Features:
- Tap to place furniture
- Drag to reposition
- 360° panorama view
- Screenshot capture"""

    # Budget calculator
    if any(w in msg for w in ["calculator", "calculate", "estimate", "renovation cost"]):
        return """💰 Budget Calculator:
Plan your interior design budget smartly!

Our calculator considers:
- Room size (sq ft)
- Quality level (Budget/Standard/Premium/Luxury)
- Room type and number of rooms

Cost breakdown:
- Furniture: 45% of budget
- Lighting: 15%
- Decor: 15%
- Paint: 10%
- Labor: 5%

Visit Budget Calculator page for exact estimates!"""

    # Nearby shops
    if any(w in msg for w in ["nearby", "near me", "shop", "store", "local", "where to buy"]):
        return """🗺️ Find Furniture Shops Near You:
Visit our Nearby Shops page to find:
- IKEA, Pepperfry, Urban Ladder
- HomeTown, Godrej Interio, Durian
- Nilkamal, @Home stores

Features:
- Search by city
- View on OpenStreetMap
- Get directions
- Compare prices"""

    # Living room
    if any(w in msg for w in ["living room", "hall", "drawing room", "lounge"]):
        return """🛋️ Living Room Design Tips:
Essential Furniture:
- Sofa (2-3 seater or L-shaped)
- Coffee Table
- TV Unit
- Accent Chair
- Floor Lamp

Layout Tips:
✅ Center sofa facing TV or fireplace
✅ Keep 90cm walkway space
✅ Use rugs to define seating area
✅ Add plants for freshness

Budget estimate: Rs.50,000 - Rs.2,00,000"""

    # Bedroom
    if any(w in msg for w in ["bedroom", "bed room", "sleeping room", "master bedroom"]):
        return """🛏️ Bedroom Design Tips:
Essential Furniture:
- Bed (King/Queen)
- Wardrobe
- Bedside Tables (2)
- Dressing Table
- Study Chair

Layout Tips:
✅ Place bed against solid wall
✅ Keep both sides of bed accessible
✅ Use mirrors to make room look bigger

Budget estimate: Rs.40,000 - Rs.1,50,000"""

    # Kitchen
    if any(w in msg for w in ["kitchen", "cooking", "dining"]):
        return """🍳 Kitchen and Dining Tips:
Essential Items:
- Dining Table + 4-6 Chairs
- Kitchen Cabinet
- Kitchen Island (optional)

The Kitchen Triangle:
- Cooktop, Sink, Refrigerator
- Should form a compact triangle

Budget estimate: Rs.60,000 - Rs.3,00,000"""

    # Office
    if any(w in msg for w in ["office", "work from home", "study", "home office", "wfh"]):
        return """💼 Home Office Design Tips:
Essential Furniture:
- Executive Desk (L-shaped or straight)
- Ergonomic Chair (invest here!)
- Bookshelf
- Good Desk Lamp

Productivity Tips:
✅ Face desk toward natural light
✅ Keep monitor at eye level
✅ Add a plant for focus

Budget estimate: Rs.25,000 - Rs.80,000"""

    # Thank you
    if any(w in msg for w in ["thank", "thanks", "thank you", "dhanyawad", "shukriya"]):
        return "You're most welcome! Feel free to ask me anything about furniture, design styles, or room planning. Happy designing! 🏠✨"

    # Goodbye
    if any(w in msg for w in ["bye", "goodbye", "see you", "later", "cya"]):
        return "Goodbye! Come back anytime for interior design help. Happy decorating your dream home! 🏠"

    # Help
    if any(w in msg for w in ["help", "what can you do", "features", "what do you know"]):
        return """🤖 I can help you with:
🛋️ Furniture - Sofas, chairs, tables, lamps, shelves
💰 Pricing - Budget planning and estimates
🎨 Design Styles - Modern, Scandinavian, Industrial, Bohemian
📸 Room Analysis - AI room photo analysis
📷 AR Camera - Visualize furniture in your room
🗺️ Nearby Shops - Find furniture stores near you
📦 Booking - How to order furniture
🚚 Delivery - Shipping and installation info

Just ask me anything about interior design!"""

    # Default intelligent response
    return f"""I understand you're asking about "{msg}". I can help you with:
- Furniture selection and pricing
- Design styles (Modern, Scandinavian, Industrial, Bohemian)
- Room planning (Living room, Bedroom, Kitchen, Office)
- Budget planning and estimates
- AR furniture visualization
- Nearby furniture shops

Could you be more specific? For example:
- "Tell me about sofas"
- "What is my budget for a living room?"
- "How do I use AR camera?"
- "What is Scandinavian style?" """


def _gemini_reply(user_message: str, language: str):
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


def _generate_audio(text: str, language: str):
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
    msg = user_message.lower().strip()

    # 1. Try Gemini AI first
    reply = _gemini_reply(user_message, language)

    # 2. Fall back to smart rule-based responses
    if not reply:
        reply = get_smart_response(msg)
        prefix = _LANG_PREFIXES.get(language, "")
        reply = prefix + reply

    # 3. Generate TTS audio
    audio_url = _generate_audio(reply, language)

    return {"text": reply, "audio_url": audio_url}
