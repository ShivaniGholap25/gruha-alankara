from datetime import timedelta
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY", "gruha-alankara-2026")

# Railway PostgreSQL gives postgres:// — SQLAlchemy needs postgresql://
# If DATABASE_URL is set but psycopg2 fails, fall back to SQLite
_db_url = os.environ.get("DATABASE_URL", "")
if _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql://", 1)
if not _db_url:
    _db_url = f"sqlite:///{os.path.join(BASE_DIR, 'gruha_alankara.db')}"
SQLALCHEMY_DATABASE_URI = _db_url
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = "uploads"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

IS_PROD = os.environ.get("FLASK_ENV") == "production"
SESSION_COOKIE_SECURE = IS_PROD
SESSION_COOKIE_SAMESITE = "None" if IS_PROD else "Lax"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = "gruha_session"
PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

os.makedirs(os.path.join(BASE_DIR, "uploads"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "static", "audio"), exist_ok=True)
