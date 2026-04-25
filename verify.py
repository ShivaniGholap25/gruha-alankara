import sys, os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from app import app, db

with app.app_context():
    db.create_all()
    print("SUCCESS: App imports fine and DB created")
    print("Flask app is ready to run!")
