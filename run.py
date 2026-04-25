import sys, os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
from app import app
from models import db
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.jinja_env.auto_reload = True
    app.run(host='0.0.0.0', port=5000, debug=True)