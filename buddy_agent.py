import os
import uuid
import random


def buddy_respond(user_message, user_id, language="en"):
    msg = user_message.lower()

    responses = {
        "book": "I have noted your furniture booking request. Our team will contact you within 24 hours to confirm your order.",
        "sofa": "Great choice! Our sofas range from Rs.8,000 to Rs.45,000. Popular options include the Luxe Comfort Sofa and Urban Corner Sofa. Would you like me to book one?",
        "table": "We have beautiful dining and coffee tables starting from Rs.5,000. The Sheesham Dining Table is our bestseller!",
        "chair": "Our chair collection includes accent chairs, lounge chairs, and dining chairs from Rs.4,000 to Rs.18,000.",
        "lamp": "Lighting can transform a room! We have pendant lamps, floor lamps, and table lamps from Rs.2,500.",
        "shelf": "Our shelving units range from Rs.6,000 to Rs.25,000. Perfect for both storage and display.",
        "price": "Our furniture is priced between Rs.5,000 and Rs.50,000. We offer EMI options and seasonal discounts.",
        "discount": "We currently offer 10% discount on orders above Rs.25,000 and free delivery on orders above Rs.15,000.",
        "delivery": "We offer free delivery within the city for orders above Rs.15,000. Delivery takes 3-7 business days.",
        "color": "I can suggest color palettes based on your chosen design style. Which style interests you most?",
        "modern": "Modern Minimalist style features clean lines, neutral colors, and functional furniture. Perfect for contemporary homes!",
        "scandinavian": "Scandinavian style uses natural materials, soft tones, and cozy textures. Very popular and timeless!",
        "budget": "Please share your budget and I will suggest the best furniture combinations within your range.",
    }

    response_text = "Hello! I am Gruha Buddy, your interior design assistant. I can help you with furniture selection, booking, pricing, and design tips. What would you like to know?"

    for keyword, resp in responses.items():
        if keyword in msg:
            response_text = resp
            break

    lang_prefixes = {
        "te": "నమస్కారం! ",
        "hi": "नमस्ते! ",
        "en": "",
    }

    prefix = lang_prefixes.get(language, "")
    final_response = prefix + response_text

    audio_url = None
    try:
        from gtts import gTTS
        audio_dir = os.path.join("static", "audio")
        os.makedirs(audio_dir, exist_ok=True)
        filename = f"buddy_{uuid.uuid4().hex[:8]}.mp3"
        filepath = os.path.join(audio_dir, filename)
        lang_code = language if language in ["en", "te", "hi"] else "en"
        tts = gTTS(text=final_response, lang=lang_code)
        tts.save(filepath)
        audio_url = f"/static/audio/{filename}"
    except Exception:
        audio_url = None

    return {
        "text": final_response,
        "audio_url": audio_url,
    }
