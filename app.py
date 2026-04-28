import sys, os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import uuid
import json
import time
import logging
import random
import jwt
from datetime import datetime
from collections import Counter
from io import BytesIO

from flask import Flask, current_app, flash, jsonify, redirect, render_template, request, send_from_directory, session, url_for
from flask_cors import CORS
try:
    import numpy as np
except Exception:
    np = None
from PIL import Image, ImageFilter, ImageStat
try:
    from sqlalchemy import text
except Exception:
    from sqlalchemy.sql import text
from werkzeug.utils import secure_filename

from ai_design import generate_design
from buddy_agent import buddy_respond
from models import db, User, Design, Furniture, Booking, init_db


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def allowed_file(filename):
    allowed_extensions = {"png", "jpg", "jpeg", "webp", "gif", "bmp", "tiff"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object("config")
    if test_config:
        app.config.update(test_config)

    frontend_url = os.environ.get("FRONTEND_URL", "")
    allowed_origins = [o for o in [
        "http://localhost:5173",
        "http://localhost:5174",
        frontend_url,
    ] if o]
    CORS(app,
         origins=allowed_origins,
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    init_db(app)

    upload_dir = os.path.join(app.root_path, app.config.get("UPLOAD_FOLDER", "uploads"))
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(os.path.join(app.root_path, "static", "audio"), exist_ok=True)

    def _parse_design_payload(raw_payload):
        if not raw_payload:
            return {}
        try:
            data = json.loads(raw_payload)
            if isinstance(data, dict):
                return data
        except Exception:
            return {}
        return {}

    def _design_to_card_dict(design):
        payload = _parse_design_payload(design.ai_output)
        style_theme = payload.get("style_theme") or design.style_theme or "Modern Minimalist"
        room_type = payload.get("room_type") or "Living Room"
        budget = payload.get("budget")
        try:
            budget = int(float(budget))
        except (TypeError, ValueError):
            budget = 5000
        design_name = payload.get("design_name") or f"Design #{design.id}"
        created_text = design.created_at.strftime("%Y-%m-%d %H:%M:%S") if design.created_at else ""
        return {
            "id": design.id,
            "title": design_name,
            "design_name": design_name,
            "room_type": room_type,
            "style_theme": style_theme,
            "budget": budget,
            "created_at": created_text,
            "image_path": design.image_path,
            "payload": payload,
        }

    def _color_name_to_hex(name):
        mapping = {
            "white": "#ffffff",
            "cream": "#fff8dc",
            "beige": "#f5f5dc",
            "grey": "#808080",
            "gray": "#808080",
            "blue": "#4169e1",
            "green": "#228b22",
            "brown": "#8b4513",
            "black": "#1a1a1a",
            "yellow": "#ffd700",
            "pink": "#ffb6c1",
        }
        if not name:
            return None
        key = str(name).strip().lower()
        if key.startswith("#") and len(key) in (4, 7):
            return key
        return mapping.get(key)

    def _parse_buddy_action(message):
        text_msg = str(message or "").strip().lower()
        if not text_msg:
            return None

        def _extract_last_word():
            parts = text_msg.replace(",", " ").split()
            return parts[-1] if parts else ""

        if "change wall to" in text_msg:
            color = _color_name_to_hex(_extract_last_word())
            if color:
                return {"type": "color", "target": "wall", "value": color}
        if text_msg.startswith("paint "):
            color = _color_name_to_hex(_extract_last_word())
            if color:
                target = "wall"
                words = text_msg.split()
                if len(words) > 1:
                    target = words[1]
                return {"type": "color", "target": target, "value": color}
        if text_msg.startswith("remove "):
            return {"type": "remove", "target": text_msg.replace("remove ", "", 1).strip(), "value": None}
        if text_msg.startswith("add "):
            return {"type": "add", "target": text_msg.replace("add ", "", 1).strip(), "value": None}
        if "brighter" in text_msg:
            return {"type": "light", "target": "ambient", "value": "up"}
        if "darker" in text_msg:
            return {"type": "light", "target": "ambient", "value": "down"}
        if "change floor to" in text_msg:
            color = _color_name_to_hex(_extract_last_word())
            if color:
                return {"type": "color", "target": "floor", "value": color}
        return None

    def _get_user_id():
        """Get user_id from JWT Bearer token (primary) or session cookie (fallback)."""
        # 1. Try Bearer token first
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            try:
                token = auth_header.split(" ", 1)[1]
                data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
                return data.get("user_id")
            except Exception:
                pass
        # 2. Fallback to session cookie
        return session.get("user_id")

    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(upload_dir, filename)

    @app.route("/api/me")
    def api_me():
        user_id = _get_user_id()
        if not user_id:
            return jsonify({"authenticated": False}), 401
        user = User.query.get(user_id)
        if not user:
            session.clear()
            return jsonify({"authenticated": False}), 401
        return jsonify({"authenticated": True, "user": {"id": user.id, "username": user.username, "email": user.email}})

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/health")
    def health():
        db.session.execute(text("SELECT 1"))
        return jsonify({
            "status": "ok",
            "db": "connected",
            "counts": {
                "users": User.query.count(),
                "designs": Design.query.count(),
                "furniture": Furniture.query.count(),
                "bookings": Booking.query.count(),
            }
        })

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            return render_template("register.html")
        payload = request.get_json(silent=True) or {}
        username = (payload.get("username") or request.form.get("username", "")).strip()
        email = (payload.get("email") or request.form.get("email", "")).strip().lower()
        password = payload.get("password") or request.form.get("password", "")
        if not username or not email or not password:
            return jsonify({"error": "All fields are required."}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email is already registered."}), 409
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"success": True, "message": "Registration successful. Please log in."})

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return redirect("http://localhost:5173/login")
        data = request.get_json(silent=True) or request.form.to_dict()
        email = str(data.get("email", "")).strip().lower()
        password = str(data.get("password", ""))

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({"success": False, "error": "Invalid email or password"}), 401

        session["user_id"] = user.id
        session["username"] = user.username
        session.permanent = True

        # Generate JWT token for cross-domain auth (Vercel → Render)
        token = jwt.encode(
            {"user_id": user.id},
            app.config["SECRET_KEY"],
            algorithm="HS256"
        )

        return jsonify({
            "success": True,
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })

    @app.route("/logout", methods=["GET", "POST"])
    def logout():
        session.clear()
        return jsonify({"success": True, "message": "Logged out successfully."})

    @app.route("/design")
    def design():
        return render_template("design.html")

    @app.route("/analyze", methods=["GET"])
    def analyze():
        return render_template("analyze.html")

    @app.route("/catalog", methods=["GET"])
    def catalog_page():
        user_id = session.get("user_id")
        if not user_id:
            flash("Please log in to view your catalog.", "error")
            return redirect(url_for("login"))
        return render_template("catalog.html")

    @app.route("/furniture")
    def furniture_page():
        return render_template("furniture.html")

    @app.route("/get-furniture")
    def get_furniture():
        items = Furniture.query.all()
        return jsonify([
            {
                "id": f.id,
                "name": f.name,
                "category": f.category,
                "price": f.price,
                "description": f.description,
                "image_url": f.image_url,
            }
            for f in items
        ])

    @app.route("/book-furniture", methods=["POST"])
    def book_furniture():
        user_id = _get_user_id()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        payload = request.get_json(silent=True) or request.form.to_dict() or {}
        furniture_id = payload.get("furniture_id")
        furniture_name = str(payload.get("furniture_name") or payload.get("name") or "").strip()

        furniture = None
        if furniture_id is not None and str(furniture_id).strip() != "":
            try:
                furniture = Furniture.query.get(int(furniture_id))
            except (TypeError, ValueError):
                furniture = None

        if not furniture and furniture_name:
            furniture = Furniture.query.filter(Furniture.name.ilike(furniture_name)).first()

        if not furniture:
            return jsonify({"error": "Furniture not found"}), 404

        booking = Booking(user_id=user_id, furniture_id=furniture.id, status="pending")
        db.session.add(booking)
        db.session.commit()
        # Immediately confirm
        booking.status = "confirmed"
        db.session.commit()
        return jsonify({"success": True, "booking_id": booking.id, "furniture_id": furniture.id, "status": "confirmed"})

    @app.route("/my-bookings")
    def my_bookings():
        user_id = _get_user_id()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.booking_date.desc()).all()
        booking_list = []
        for b in bookings:
            furniture = Furniture.query.get(b.furniture_id)
            booking_list.append(
                {
                    "id": b.id,
                    "furniture_name": furniture.name if furniture else "Unknown",
                    "furniture_category": furniture.category if furniture else "",
                    "price": furniture.price if furniture else 0,
                    "status": b.status,
                    "date": b.booking_date.strftime("%Y-%m-%d %H:%M") if b.booking_date else "",
                }
            )

        return jsonify(booking_list)

    @app.route("/cancel-booking/<int:id>", methods=["POST"])
    def cancel_booking(id):
        user_id = _get_user_id()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        booking = Booking.query.filter_by(id=id, user_id=user_id).first()
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        booking.status = "cancelled"
        db.session.commit()
        return jsonify({"success": True})

    @app.route("/live_ar", methods=["GET"])
    def live_ar():
        return render_template("live_ar_camera.html")

    @app.route("/nearby-shops")
    def nearby_shops():
        return render_template("nearby_shops.html")

    @app.route("/budget-calculator")
    def budget_calculator():
        return render_template("budget_calculator.html")

    @app.route("/gallery")
    def gallery():
        return render_template("gallery.html")

    @app.route("/style-quiz")
    def style_quiz():
        return render_template("style_quiz.html")

    @app.route("/dashboard")
    def dashboard():
        user_id = session.get("user_id")
        if not user_id:
            flash("Please log in to view your dashboard.", "error")
            return redirect(url_for("login"))
        user = User.query.filter_by(id=user_id).first()
        designs = Design.query.filter_by(user_id=user_id).order_by(Design.created_at.desc()).all()
        bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.booking_date.desc()).all()
        return render_template("dashboard.html", designs=designs, bookings=bookings, user=user)

    @app.route("/dashboard/stats", methods=["GET"])
    def dashboard_stats():
        user_id = _get_user_id()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        designs = Design.query.filter_by(user_id=user_id).order_by(Design.created_at.desc()).all()
        bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.booking_date.desc()).all()

        style_counter = Counter()
        room_counter = Counter()
        recent_designs = []

        for design in designs:
            payload = _parse_design_payload(design.ai_output)
            style = payload.get("style_theme") or design.style_theme or "Unknown"
            room = payload.get("room_type") or "Unknown"
            style_counter[style] += 1
            room_counter[room] += 1
            recent_designs.append({
                "id": design.id,
                "style_theme": style,
                "room_type": room,
                "created_at": design.created_at.isoformat() if design.created_at else "",
                "image_path": design.image_path,
                "title": payload.get("design_name") or f"Design #{design.id}",
            })

        favorite_style = style_counter.most_common(1)[0][0] if style_counter else "-"
        most_used_room = room_counter.most_common(1)[0][0] if room_counter else "-"

        timeline = []
        for d in designs[:8]:
            timeline.append({
                "type": "design",
                "label": f"Created design #{d.id}",
                "timestamp": d.created_at.isoformat() if d.created_at else "",
            })
        for b in bookings[:8]:
            furniture_name = b.furniture.name if b.furniture else "Furniture"
            timeline.append({
                "type": "booking",
                "label": f"Booking #{b.id} for {furniture_name} ({b.status})",
                "timestamp": b.booking_date.isoformat() if b.booking_date else "",
            })
        timeline.sort(key=lambda item: item.get("timestamp", ""), reverse=True)

        return jsonify({
            "total_designs": len(designs),
            "total_bookings": len(bookings),
            "favorite_style": favorite_style,
            "most_used_room": most_used_room,
            "recent_designs": recent_designs[:4],
            "recent_bookings": [
                {
                    "id": b.id,
                    "furniture": b.furniture.name if b.furniture else "N/A",
                    "status": b.status,
                    "booking_date": b.booking_date.isoformat() if b.booking_date else "",
                }
                for b in bookings[:6]
            ],
            "timeline": timeline[:8],
        })

    @app.route("/get-designs", methods=["GET"])
    def get_designs():
        user_id = _get_user_id()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        designs = Design.query.filter_by(user_id=user_id).order_by(Design.created_at.desc()).all()
        return jsonify([_design_to_card_dict(d) for d in designs])

    @app.route("/design-config/<int:design_id>", methods=["GET"])
    def design_config(design_id):
        user_id = _get_user_id()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        design = Design.query.filter_by(id=design_id, user_id=user_id).first()
        if not design:
            return jsonify({"error": "Design not found"}), 404
        return jsonify(_design_to_card_dict(design))

    @app.route("/delete-design/<int:id>", methods=["DELETE"])
    def delete_design(id):
        user_id = _get_user_id()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        design = Design.query.filter_by(id=id, user_id=user_id).first()
        if not design:
            return jsonify({"error": "Design not found"}), 404
        db.session.delete(design)
        db.session.commit()
        return jsonify({"success": True})

    @app.route("/duplicate-design/<int:id>", methods=["POST"])
    def duplicate_design(id):
        user_id = _get_user_id()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        source = Design.query.filter_by(id=id, user_id=user_id).first()
        if not source:
            return jsonify({"error": "Design not found"}), 404
        source_payload = _parse_design_payload(source.ai_output)
        source_name = source_payload.get("design_name") or f"Design #{source.id}"
        source_payload["design_name"] = f"Copy of {source_name}"
        clone = Design(
            user_id=user_id,
            image_path=source.image_path,
            style_theme=source.style_theme,
            ai_output=json.dumps(source_payload),
        )
        db.session.add(clone)
        db.session.commit()
        return jsonify({"success": True, "new_id": clone.id})

    @app.route("/generate-design", methods=["POST"])
    def generate_design_route():
        payload = request.get_json(silent=True) or {}
        style_theme = str(payload.get("style_theme") or request.args.get("style") or "Modern Minimalist")
        room_type = str(payload.get("room_type") or request.args.get("room_type") or "Living Room")
        color_theme = str(payload.get("color_theme") or "Warm Neutrals")
        try:
            budget = int(float(payload.get("budget") or "50000"))
        except (TypeError, ValueError):
            budget = 50000

        style_data = {
            "Modern Minimalist": {
                "desc": "Clean lines, neutral colors, and functional furniture with minimal clutter",
                "colors": ["#FFFFFF", "#000000", "#808080", "#F5F5F5"],
                "materials": ["Glass", "Steel", "Concrete", "Light wood"],
                "story": "Your space focuses on clean geometry and breathable movement with understated luxury.",
            },
            "Scandinavian": {
                "desc": "Bright airy spaces with natural materials and cozy textures",
                "colors": ["#F5F0E8", "#2C5F2E", "#D4A373", "#FEFAE0"],
                "materials": ["Pine wood", "Linen", "Wool", "Ceramic"],
                "story": "Soft layers and warm daylight create an inviting everyday living environment.",
            },
            "Industrial": {
                "desc": "Raw materials with urban character balancing exposed textures",
                "colors": ["#2E2E2E", "#5A5A5A", "#8C7B75", "#B0A8A0"],
                "materials": ["Raw steel", "Exposed brick", "Concrete", "Distressed wood"],
                "story": "A bold urban vibe with layered metal and wood for confident visual rhythm.",
            },
            "Bohemian": {
                "desc": "Eclectic mix of colors and textures with expressive accents",
                "colors": ["#E76F51", "#2A9D8F", "#E9C46A", "#F4A261"],
                "materials": ["Rattan", "Jute", "Cotton weave", "Carved wood"],
                "story": "Artful detailing and layered textures bring a relaxed, story-driven ambiance.",
            },
            "Traditional": {
                "desc": "Classic elegance with rich details and timeless finishes",
                "colors": ["#7A4E2D", "#C9B79C", "#8B0000", "#F5E6CC"],
                "materials": ["Teak wood", "Brass", "Velvet", "Marble"],
                "story": "Timeless silhouettes and refined accents elevate formality and comfort together.",
            },
            "Contemporary": {
                "desc": "Current trend-forward styling with flexible furniture",
                "colors": ["#D9D9D9", "#4A4E69", "#9A8C98", "#F2E9E4"],
                "materials": ["Tempered glass", "Matte metal", "Engineered wood", "Textured fabric"],
                "story": "Balanced contrast and adaptive pieces keep the room current and highly functional.",
            },
        }
        sd = style_data.get(style_theme, style_data["Modern Minimalist"])

        room_furniture = {
            "Living Room": ["Sofa", "Coffee Table", "TV Unit", "Accent Chair", "Floor Lamp"],
            "Bedroom": ["Bed", "Wardrobe", "Bedside Tables", "Dressing Table", "Study Chair"],
            "Kitchen": ["Cabinet", "Dining Table", "Dining Chairs", "Island", "Bar Stools"],
            "Bathroom": ["Vanity", "Mirror Cabinet", "Towel Rack", "Storage Shelf", "Stool"],
            "Office": ["Executive Desk", "Ergonomic Chair", "Bookshelf", "File Cabinet", "Desk Lamp"],
            "Dining Room": ["Dining Table", "Chairs", "Sideboard", "Display Cabinet", "Pendant Light"],
        }
        selected_furniture = room_furniture.get(room_type, room_furniture["Living Room"])
        priority_tags = ["High", "High", "Medium", "Medium", "Low"]

        furniture_list = []
        for idx, name in enumerate(selected_furniture):
            price = int((budget * 0.45) / max(1, len(selected_furniture)))
            price += idx * 1500
            furniture_list.append({
                "id": f"f_{idx+1}",
                "name": name,
                "price": price,
                "price_inr": price,
                "material": sd["materials"][idx % len(sd["materials"])],
                "category": room_type.lower().replace(" ", "_"),
                "priority": priority_tags[idx % len(priority_tags)],
                "position": {"x": 0, "y": 0, "z": 0},
            })

        furniture_total = int(budget * 0.45)
        lighting_total = int(budget * 0.15)
        decor_total = int(budget * 0.15)
        paint_total = int(budget * 0.10)
        labor_total = int(budget * 0.10)
        contingency_total = max(0, budget - (furniture_total + lighting_total + decor_total + paint_total + labor_total))

        budget_breakdown = [
            {"category": "Furniture", "percent": 45, "amount": furniture_total},
            {"category": "Lighting", "percent": 15, "amount": lighting_total},
            {"category": "Decor", "percent": 15, "amount": decor_total},
            {"category": "Paint", "percent": 10, "amount": paint_total},
            {"category": "Labor", "percent": 10, "amount": labor_total},
            {"category": "Contingency", "percent": 5, "amount": contingency_total},
        ]

        return jsonify({
            "style": style_theme,
            "style_theme": style_theme,
            "room_type": room_type,
            "budget": budget,
            "color_theme": color_theme,
            "description": sd["desc"],
            "furniture": selected_furniture,
            "furniture_list": furniture_list,
            "colors": sd["colors"],
            "materials": sd["materials"],
            "ai_story": sd["story"],
            "layout_tips": [
                "Maintain clear movement pathways.",
                "Balance visual weight across the room.",
                "Layer task and ambient lighting.",
            ],
            "budget_split": budget_breakdown,
            "budget_breakdown": budget_breakdown,
            "savings_tips": [
                "Reuse one existing furniture piece to reduce spend.",
                "Buy lighting in combos for better unit pricing.",
                "Reserve 5% contingency for final styling upgrades.",
            ],
            "ai_status": "AI Design Complete",
        })

    @app.route("/save-design", methods=["POST"])
    def save_design():
        user_id = _get_user_id()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        payload = request.get_json(silent=True) or {}
        design_name = str(payload.get("name", "")).strip() or f"{payload.get('style_theme', 'Design')} Concept"
        style_theme = str(payload.get("style_theme", "Modern Minimalist")).strip()
        room_type = str(payload.get("room_type", "Living Room")).strip()
        try:
            budget = int(float(payload.get("budget", 5000)))
        except (TypeError, ValueError):
            budget = 5000
        payload["design_name"] = design_name
        payload["style_theme"] = style_theme
        payload["room_type"] = room_type
        payload["budget"] = budget
        design = Design(
            user_id=user_id,
            image_path="uploads/preview.jpg",
            style_theme=style_theme,
            ai_output=json.dumps(payload),
        )
        db.session.add(design)
        db.session.commit()
        return jsonify({"success": True, "design_id": design.id})

    @app.route("/preview-composite", methods=["POST"])
    def preview_composite():
        """Overlay furniture labels on the uploaded room image using PIL."""
        payload = request.get_json(silent=True) or {}
        image_path_rel = payload.get("image_path", "")
        furniture_names = payload.get("furniture_names", [])[:3]

        if not image_path_rel:
            return jsonify({"error": "image_path required"}), 400

        full_path = os.path.join(app.root_path, image_path_rel.lstrip("/"))
        if not os.path.exists(full_path):
            return jsonify({"error": "Image not found"}), 404

        try:
            from PIL import ImageDraw, ImageFont
            img = Image.open(full_path).convert("RGB")
            draw = ImageDraw.Draw(img, "RGBA")
            iw, ih = img.size

            colors_overlay = [
                (124, 58, 237, 160),   # purple
                (16, 185, 129, 160),   # green
                (245, 158, 11, 160),   # amber
            ]

            zone_h = ih // max(len(furniture_names), 1)
            for idx, name in enumerate(furniture_names):
                x0 = int(iw * 0.05)
                y0 = int(ih * 0.1) + idx * zone_h
                x1 = int(iw * 0.45)
                y1 = y0 + int(zone_h * 0.6)
                color = colors_overlay[idx % len(colors_overlay)]
                draw.rectangle([x0, y0, x1, y1], fill=color, outline=(255, 255, 255, 200), width=2)

                # Label
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", max(16, iw // 40))
                except Exception:
                    font = ImageFont.load_default()

                draw.text((x0 + 10, y0 + 10), name, fill=(255, 255, 255, 255), font=font)

            previews_dir = os.path.join(upload_dir, "previews")
            os.makedirs(previews_dir, exist_ok=True)
            out_name = f"preview_{uuid.uuid4().hex[:8]}.jpg"
            out_path = os.path.join(previews_dir, out_name)
            img.save(out_path, "JPEG", quality=85)

            return jsonify({"preview_url": f"/uploads/previews/{out_name}"})

        except Exception as e:
            logger.exception("Composite preview failed: %s", e)
            return jsonify({"error": "Failed to generate preview"}), 500

    @app.route("/uploads/previews/<path:filename>")
    def uploaded_preview(filename):
        return send_from_directory(os.path.join(upload_dir, "previews"), filename)

    @app.route("/analyze-room", methods=["POST"])
    def analyze_room():
        file = request.files.get("image") or request.files.get("room_image")
        if not file or not file.filename:
            return jsonify({"error": "No image file provided"}), 400
        if not allowed_file(file.filename):
            return jsonify({"error": "Unsupported file type. Use PNG, JPG or JPEG"}), 400

        raw_bytes = file.read()

        # Issue 8 — size validation
        if len(raw_bytes) > 5 * 1024 * 1024:
            return jsonify({"error": "File too large. Maximum size is 5 MB."}), 400

        # Issue 8 — MIME validation
        allowed_mime = {"image/jpeg", "image/png", "image/webp"}
        mime = file.mimetype or ""
        if mime and mime not in allowed_mime:
            return jsonify({"error": "Unsupported file type. Use JPEG, PNG or WEBP."}), 400

        try:
            image = Image.open(BytesIO(raw_bytes)).convert("RGB")
            w, h = image.size

            # Issue 8 — minimum dimensions
            if w < 100 or h < 100:
                return jsonify({"error": "Image too small. Please upload a larger photo."}), 400

            # ── Save image so Claude can read it ──────────────────────────
            import uuid as _uuid
            ext = secure_filename(file.filename).rsplit(".", 1)[-1].lower() if "." in file.filename else "jpg"
            tmp_name = f"analyze_{_uuid.uuid4().hex}.{ext}"
            tmp_path = os.path.join(upload_dir, tmp_name)
            with open(tmp_path, "wb") as fh:
                fh.write(raw_bytes)

            # ── Issue 1 — Claude vision analysis ─────────────────────────
            from ai_design import analyze_room_with_vision, NOT_A_ROOM as _NOT_A_ROOM
            vision_result = analyze_room_with_vision(tmp_path)

            if vision_result == _NOT_A_ROOM:
                return jsonify({"error": "Please upload a photo of a room interior."}), 400

            if isinstance(vision_result, dict):
                # Return Claude's rich result
                return jsonify({
                    "source": "claude",
                    "room_type": vision_result.get("room_type", "Unknown"),
                    "style": vision_result.get("style", "Modern"),
                    "dimensions": {"width": round(w * 0.05, 2), "length": round(h * 0.05, 2), "height": 9.0, "area": round(w * 0.05 * h * 0.05, 2)},
                    "colors": vision_result.get("detected_colors", []),
                    "furniture_suggestions": vision_result.get("furniture_suggestions", []),
                    "layout_tip": vision_result.get("layout_tip", ""),
                    "lighting": {"quality": "Good", "brightness": int(ImageStat.Stat(image.convert("L")).mean[0])},
                    "style_recommendations": [{"style": vision_result.get("style", "Modern"), "score": 95.0}],
                    "image_path": f"uploads/{tmp_name}",
                })

            # ── PIL fallback (no Claude key or error) ─────────────────────
            width_ft = round(w * 0.05, 2)
            length_ft = round(h * 0.05, 2)
            area = round(width_ft * length_ft, 2)
            brightness = int(ImageStat.Stat(image.convert("L")).mean[0])
            lighting_quality = "Excellent" if brightness >= 170 else "Good" if brightness >= 120 else "Moderate" if brightness >= 80 else "Low"
            quantized = image.quantize(5)
            palette = quantized.getpalette() or []
            colors = [f"#{palette[i*3]:02x}{palette[i*3+1]:02x}{palette[i*3+2]:02x}" for i in range(5) if len(palette) >= (i+1)*3]
            while len(colors) < 5:
                colors.append("#2a2f45")

            style_reference = {
                "Modern Minimalist": ["#FFFFFF", "#000000", "#808080", "#F5F5F5"],
                "Scandinavian": ["#F5F0E8", "#D4A373", "#CCD5AE", "#E9EDC9"],
                "Industrial": ["#2E2E2E", "#5A5A5A", "#8C7B75", "#B0A8A0"],
                "Bohemian": ["#E76F51", "#2A9D8F", "#E9C46A", "#F4A261"],
                "Contemporary": ["#D9D9D9", "#4A4E69", "#9A8C98", "#F2E9E4"],
            }

            def _rgb(hex_color):
                v = hex_color.lstrip("#")
                return tuple(int(v[i:i+2], 16) for i in (0, 2, 4))

            def _style_score(style_colors):
                room_rgbs = [_rgb(c) for c in colors[:4]]
                style_rgbs = [_rgb(c) for c in style_colors]
                score = 0
                for room_rgb in room_rgbs:
                    min_dist = min(abs(room_rgb[0]-s[0])+abs(room_rgb[1]-s[1])+abs(room_rgb[2]-s[2]) for s in style_rgbs)
                    score += max(0, 255 - (min_dist / 3))
                return round((score / (len(room_rgbs) * 255)) * 100, 1)

            style_scores = [{"style": s, "score": _style_score(c)} for s, c in style_reference.items()]
            style_scores.sort(key=lambda x: x["score"], reverse=True)

            return jsonify({
                "source": "pil",
                "dimensions": {"width": width_ft, "length": length_ft, "height": 9.0, "area": area},
                "lighting": {"quality": lighting_quality, "brightness": brightness, "description": "Consider warm accent lights for evening ambiance."},
                "colors": colors,
                "features": {"complexity": "Medium", "edges": random.randint(3000, 5000), "orientation": "Landscape" if w >= h else "Portrait"},
                "style_recommendations": style_scores[:3],
                "image_path": f"uploads/{tmp_name}",
            })

        except Exception as e:
            logger.exception("Room analysis failed: %s", e)
            return jsonify({"error": "Failed to analyze image"}), 500

    @app.route("/upload", methods=["POST"])
    def upload_room_image():
        user_id = session.get("user_id")
        file = request.files.get("room_image") or request.files.get("image")
        if not file or not file.filename:
            return jsonify({"error": "No image file provided"}), 400
        if not allowed_file(file.filename):
            return jsonify({"error": "Unsupported file type"}), 400
        ext = secure_filename(file.filename).rsplit(".", 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        file.save(os.path.join(upload_dir, unique_filename))
        style_theme = request.form.get("style_theme", "Modern")
        relative_path = os.path.join(app.config.get("UPLOAD_FOLDER", "uploads"), unique_filename)
        design_result = generate_design(os.path.join(app.root_path, relative_path), style_theme)
        if user_id:
            design = Design(user_id=user_id, image_path=relative_path, style_theme=style_theme, ai_output=json.dumps(design_result))
            db.session.add(design)
            db.session.commit()
        response_payload = {
            "message": "Image uploaded successfully",
            "design_id": design.id if user_id else None,
            "recommendations": design_result,
                "redirect": url_for("design"),
            "image_path": relative_path.replace("\\", "/"),
        }
        if isinstance(design_result, dict):
            for key in ("furniture", "color_scheme", "placement_tips", "layout", "budget"):
                if key in design_result:
                    response_payload[key] = design_result.get(key)
        return jsonify(response_payload)

    @app.route("/buddy", methods=["POST"])
    def buddy_chat():
        user_id = _get_user_id()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        payload = request.get_json(silent=True) or {}
        message = str(payload.get("message", "")).strip()
        language = str(payload.get("language", "en")).strip()
        if not message:
            return jsonify({"error": "message is required"}), 400
        action = _parse_buddy_action(message)
        base = buddy_respond(message, user_id, language)
        reply_text = "Namaste! I am Alankara. " + (base.get("text") or "Share your preferred room change and I will help.")
        return jsonify({
            "text": reply_text,
            "reply": reply_text,
            "audio_url": base.get("audio_url"),
            "action": action,
        })

    @app.route("/seed-db")
    def seed_db():
        if Furniture.query.count() > 0:
            return jsonify({"message": "Furniture catalog already has items.", "count": Furniture.query.count()})
        items = [
            Furniture(name="Luxe Comfort Sofa", category="sofa", price=18500, image_url="", description="Three-seater fabric sofa."),
            Furniture(name="Urban Corner Sofa", category="sofa", price=32000, image_url="", description="L-shaped sofa."),
            Furniture(name="Sheesham Dining Table", category="table", price=27500, image_url="", description="Solid wood dining table."),
            Furniture(name="Minimal Coffee Table", category="table", price=9500, image_url="", description="Compact coffee table."),
            Furniture(name="Nordic Accent Chair", category="chair", price=7800, image_url="", description="Single accent chair."),
            Furniture(name="Ergo Lounge Chair", category="chair", price=14200, image_url="", description="Curved lounge chair."),
            Furniture(name="Pendant Glow Lamp", category="lamp", price=5600, image_url="", description="Warm white hanging lamp."),
            Furniture(name="Tripod Floor Lamp", category="lamp", price=11200, image_url="", description="Tall floor lamp."),
            Furniture(name="Modular Wall Shelf", category="shelf", price=8600, image_url="", description="Floating shelf set."),
            Furniture(name="Industrial Book Shelf", category="shelf", price=22800, image_url="", description="Metal and wood bookshelf."),
        ]
        db.session.add_all(items)
        db.session.commit()
        return jsonify({"success": True, "message": f"Seeded {len(items)} items.", "count": len(items)})

    @app.errorhandler(404)
    def not_found(e):
        if request.path.startswith('/api') or request.is_json:
            return jsonify({"error": "Not found"}), 404
        return render_template("error.html", code=404, message="Page not found."), 404

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        if request.path.startswith('/api') or request.is_json:
            return jsonify({"error": "Internal server error"}), 500
        return render_template("error.html", code=500, message="Something went wrong."), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
