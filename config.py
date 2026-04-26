import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "gruha-alankara-2026"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'gruha_alankara.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = "uploads"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = "gruha_session"
PERMANENT_SESSION_LIFETIME = 86400

os.makedirs(os.path.join(BASE_DIR, "uploads"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "static", "audio"), exist_ok=True)

