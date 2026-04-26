import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Use env var in production, fallback to local for dev
SECRET_KEY = os.environ.get("SECRET_KEY", "gruha-alankara-2026")

# SQLite for both dev and Render (Render has ephemeral disk, good for demo)
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{os.path.join(BASE_DIR, 'gruha_alankara.db')}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = "uploads"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
SESSION_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production"
SESSION_COOKIE_SAMESITE = "None" if os.environ.get("FLASK_ENV") == "production" else "Lax"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = "gruha_session"
PERMANENT_SESSION_LIFETIME = 86400

os.makedirs(os.path.join(BASE_DIR, "uploads"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "static", "audio"), exist_ok=True)
