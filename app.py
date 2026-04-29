import sys, os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import uuid
import json
import time
import logging
import random
import jwt
from authlib.integrations.flask_client import OAuth
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

from ai_design import generate_design, analyze_room_image
from buddy_agent import buddy_respond
from models import db, User, Design, Furniture, Booking, Cart, Order, OrderItem, init_db


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
        "https://web-production-3fbd6.up.railway.app",
        frontend_url,
    ] if o]
    CORS(app,
         origins=allowed_origins,
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    init_db(app)

    # ── Google OAuth ──────────────────────────────────────────────────────
    oauth = OAuth(app)
    google = oauth.register(
        name="google",
        client_id=os.environ.get("GOOGLE_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    @app.route("/auth/google")
    def google_login():
        # Always use the exact registered callback URL
        callback = os.environ.get(
            "GOOGLE_CALLBACK_URL",
            "https://web-production-3fbd6.up.railway.app/auth/google/callback"
        )
        return google.authorize_redirect(callback)

    @app.route("/auth/google/callback")
    def google_callback():
        try:
            token = google.authorize_access_token()
            user_info = token.get("userinfo")
            if not user_info:
                return redirect("/?error=google_failed")

            email    = user_info["email"]
            name     = user_info.get("name", email.split("@")[0])
            username = name.replace(" ", "").lower()[:30]

            # Find or create user
            user = User.query.filter_by(email=email).first()
            if not user:
                # Make username unique
                base = username
                counter = 1
                while User.query.filter_by(username=username).first():
                    username = f"{base}{counter}"
                    counter += 1
                user = User(username=username, email=email)
                user.set_password(os.urandom(24).hex())  # random password
                db.session.add(user)
                db.session.commit()

            session["user_id"]  = user.id
            session["username"] = user.username
            session.permanent   = True

            # Redirect to frontend
            frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:5173")
            is_prod = os.environ.get("FLASK_ENV") == "production"
            if is_prod:
                return redirect("/")
            return redirect(f"{frontend_url}/")

        except Exception as e:
            logger.exception("Google OAuth callback failed: %s", e)
            return redirect("/?error=google_failed")

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

    def _serve_react():
        """Serve React SPA index.html."""
        react_dir = os.path.join(app.root_path, "static", "react")
        index_path = os.path.join(react_dir, "index.html")
        if os.path.exists(index_path):
            return send_from_directory(react_dir, "index.html")
        return render_template("index.html")

    @app.route("/")
    def index():
        return _serve_react()

    @app.route("/app", defaults={"path": ""})
    @app.route("/app/<path:path>")
    def serve_react(path):
        react_dir = os.path.join(app.root_path, "static", "react")
        file_path = os.path.join(react_dir, path)
        if path and os.path.exists(file_path):
            return send_from_directory(react_dir, path)
        return _serve_react()

    # ── All React page routes → serve SPA ────────────────────────────────
    for _react_path in [
        "/dashboard", "/design", "/analyze", "/catalog",
        "/furniture", "/budget-calculator",
        "/gallery", "/nearby-shops", "/live-ar", "/cart-page",
    ]:
        app.add_url_rule(_react_path, endpoint=f"react_{_react_path.strip('/')}", view_func=_serve_react)

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
            return _serve_react()
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
            return _serve_react()
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
        # GET = browser visit → redirect to homepage
        if request.method == "GET":
            return redirect("/")
        return jsonify({"success": True, "message": "Logged out successfully."})

    @app.route("/design")
    def design():
        return _serve_react()

    @app.route("/analyze", methods=["GET"])
    def analyze():
        return _serve_react()

    @app.route("/catalog", methods=["GET"])
    def catalog_page():
        return _serve_react()

    @app.route("/furniture")
    def furniture_page():
        return _serve_react()

    @app.route("/cart-page")
    def cart_page():
        return _serve_react()

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
    def my_bookings_page():
        return _serve_react()

    @app.route("/api/my-bookings")
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

    @app.route("/live-ar")
    def live_ar():
        return _serve_react()

    @app.route("/nearby-shops")
    def nearby_shops():
        return _serve_react()

    @app.route("/budget-calculator")
    def budget_calculator():
        return _serve_react()

    @app.route("/gallery")
    def gallery():
        return _serve_react()

    @app.route("/dashboard")
    def dashboard():
        return _serve_react()

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
        room_type   = str(payload.get("room_type") or request.args.get("room_type") or "Living Room")
        color_theme = str(payload.get("color_theme") or "Warm Neutrals")
        try:
            budget = int(float(payload.get("budget") or "50000"))
        except (TypeError, ValueError):
            budget = 50000

        result = generate_design(style_theme, budget, room_type)

        # Normalise keys so the frontend always gets what it expects
        result.setdefault("style", style_theme)
        result.setdefault("style_theme", style_theme)
        result.setdefault("room_type", room_type)
        result.setdefault("budget", budget)
        result.setdefault("color_theme", color_theme)
        result.setdefault("ai_status", "AI Design Complete")

        # Build furniture_list from furniture array for frontend compatibility
        raw_furniture = result.get("furniture", [])
        furniture_list = []
        for idx, item in enumerate(raw_furniture):
            if isinstance(item, dict):
                furniture_list.append({
                    "id": f"f_{idx+1}",
                    "name": item.get("name", ""),
                    "price": item.get("price_inr", 0),
                    "price_inr": item.get("price_inr", 0),
                    "material": (result.get("materials") or [""])[idx % max(len(result.get("materials") or [""]), 1)],
                    "category": room_type.lower().replace(" ", "_"),
                    "priority": item.get("priority", "recommended"),
                    "position": {"x": 0, "y": 0, "z": 0},
                })
            else:
                furniture_list.append({
                    "id": f"f_{idx+1}",
                    "name": str(item),
                    "price": 0, "price_inr": 0,
                    "material": "", "category": room_type.lower().replace(" ", "_"),
                    "priority": "recommended", "position": {"x": 0, "y": 0, "z": 0},
                })

        result["furniture_list"] = furniture_list
        result.setdefault("furniture", [f["name"] for f in furniture_list])

        # budget_split alias
        result.setdefault("budget_split", result.get("budget_breakdown", []))
        result.setdefault("layout_tips", result.get("layout_tips", []))
        result.setdefault("savings_tips", result.get("savings_tips", []))

        return jsonify(result)

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

            # ── Gemini vision analysis (falls back to PIL if no key) ──────
            result = analyze_room_image(tmp_path)

            if result.get("error") == "not_a_room":
                return jsonify({"error": result["message"]}), 422

            if result.get("error"):
                return jsonify({"error": result["error"]}), 400

            # Merge PIL-computed dimensions/brightness into Gemini result
            brightness = int(ImageStat.Stat(image.convert("L")).mean[0])
            if "dimensions" not in result:
                result["dimensions"] = {
                    "width": round(w * 0.05, 2),
                    "length": round(h * 0.05, 2),
                    "height": 9.0,
                    "area": round(w * 0.05 * h * 0.05, 2),
                }
            if "lighting" not in result:
                result["lighting"] = {"quality": "Good", "brightness": brightness, "description": "Estimated via image analysis"}
            result["image_path"] = f"uploads/{tmp_name}"
            result["style_recommendations"] = [
                {"style": result.get("style_hint", "Modern Minimalist"), "score": 95.0}
            ]
            return jsonify(result)

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
        user_id = _get_user_id()   # None for guests — allowed
        payload = request.get_json(silent=True) or {}
        message = str(payload.get("message", "")).strip()
        language = str(payload.get("language", "en")).strip()
        if not message:
            return jsonify({"text": "Please type a message.", "reply": "Please type a message.", "audio_url": None, "action": None})
        action = _parse_buddy_action(message)
        base = buddy_respond(message, user_id, language)
        reply_text = "Namaste! I am Alankara. " + (base.get("text") or "Share your preferred room change and I will help.")
        if not user_id:
            reply_text = "You are using guest mode. " + reply_text
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

    @app.route("/add-to-cart", methods=["POST"])
    def add_to_cart():
        if "user_id" not in session:
            return jsonify({"error": "Login required"}), 401
        data = request.get_json(silent=True) or {}
        furniture_id = data.get("furniture_id")
        if not furniture_id:
            return jsonify({"error": "furniture_id required"}), 400
        item = Cart.query.filter_by(user_id=session["user_id"], furniture_id=furniture_id).first()
        if item:
            item.quantity += 1
        else:
            item = Cart(user_id=session["user_id"], furniture_id=furniture_id, quantity=1)
            db.session.add(item)
        db.session.commit()
        return jsonify({"success": True})

    @app.route("/cart")
    def get_cart():
        if "user_id" not in session:
            return jsonify([])
        items = Cart.query.filter_by(user_id=session["user_id"]).all()
        return jsonify([
            {
                "id":       item.id,
                "name":     item.furniture.name,
                "price":    item.furniture.price,
                "quantity": item.quantity,
            }
            for item in items
        ])

    @app.route("/remove-from-cart/<int:id>", methods=["POST"])
    def remove_from_cart(id):
        if "user_id" not in session:
            return jsonify({"error": "Login required"}), 401
        item = Cart.query.get(id)
        if item and item.user_id == session["user_id"]:
            db.session.delete(item)
            db.session.commit()
        return jsonify({"success": True})

    @app.route("/checkout", methods=["POST"])
    def checkout():
        if "user_id" not in session:
            return jsonify({"error": "Login required"}), 401
        items = Cart.query.filter_by(user_id=session["user_id"]).all()
        if not items:
            return jsonify({"error": "Cart is empty"}), 400
        total = sum(i.quantity * i.furniture.price for i in items)
        order = Order(user_id=session["user_id"], total_amount=total)
        db.session.add(order)
        db.session.flush()
        for i in items:
            db.session.add(OrderItem(
                order_id=order.id,
                furniture_id=i.furniture_id,
                quantity=i.quantity,
                price=i.furniture.price,
            ))
        Cart.query.filter_by(user_id=session["user_id"]).delete()
        db.session.commit()
        return jsonify({"success": True, "order_id": order.id, "total": total})

    # ── Session-based cart helpers (used by furniture page quick-cart) ────────
    @app.route("/session-cart/add", methods=["POST"])
    def session_cart_add():
        data = request.get_json(silent=True) or {}
        fid  = data.get("furniture_id")
        if not fid:
            return jsonify({"error": "furniture_id required"}), 400
        cart = session.get("cart", [])
        cart.append(int(fid))
        session["cart"] = cart
        session.modified = True
        return jsonify({"success": True, "cart_count": len(cart)})

    @app.route("/session-cart")
    def session_cart_get():
        cart = session.get("cart", [])
        if not cart:
            return jsonify([])
        items = Furniture.query.filter(Furniture.id.in_(cart)).all()
        id_map = {i.id: i for i in items}
        result = []
        for fid in cart:
            item = id_map.get(fid)
            if item:
                result.append({"id": item.id, "name": item.name,
                                "price": item.price, "category": item.category})
        return jsonify(result)

    @app.route("/session-cart/remove/<int:item_id>", methods=["POST"])
    def session_cart_remove(item_id):
        cart = session.get("cart", [])
        if item_id in cart:
            cart.remove(item_id)
            session["cart"] = cart
            session.modified = True
        return jsonify({"success": True, "cart_count": len(cart)})

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
