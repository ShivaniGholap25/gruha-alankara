import io
import os
import tempfile
import unittest
from unittest.mock import patch

from app import create_app
from models import Furniture, User, db


class GruhaAlankaraAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-secret",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "UPLOAD_FOLDER": self.temp_dir.name,
                "MAX_CONTENT_LENGTH": 16 * 1024 * 1024,
            }
        )
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            user = User(username="seeduser", email="seed@example.com")
            user.set_password("password123")
            db.session.add(user)

            db.session.add_all(
                [
                    Furniture(name="Comfy Sofa", category="sofa", price=18000, image_url="https://via.placeholder.com/200", description="Demo sofa"),
                    Furniture(name="Oak Table", category="table", price=12000, image_url="https://via.placeholder.com/200", description="Demo table"),
                    Furniture(name="Reading Lamp", category="lamp", price=6000, image_url="https://via.placeholder.com/200", description="Demo lamp"),
                ]
            )
            db.session.commit()
            self.seed_user_id = user.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.temp_dir.cleanup()

    def login_seed_user(self):
        return self.client.post(
            "/login",
            data={"email": "seed@example.com", "password": "password123"},
            follow_redirects=False,
        )

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post(
            "/register",
            data={"username": "newuser", "email": "new@example.com", "password": "testpass"},
            follow_redirects=False,
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers.get("Location", ""))

    def test_register_duplicate(self):
        response = self.client.post(
            "/register",
            data={"username": "other", "email": "seed@example.com", "password": "testpass"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Email is already registered.", response.data)

    def test_login_valid(self):
        response = self.login_seed_user()
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response.headers.get("Location", ""))

        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get("user_id"), self.seed_user_id)

    def test_login_invalid(self):
        response = self.client.post(
            "/login",
            data={"email": "seed@example.com", "password": "wrong-pass"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid email or password.", response.data)

    def test_design_requires_login(self):
        response = self.client.get("/design", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers.get("Location", ""))

    @patch("app.generate_design")
    def test_file_upload(self, mock_generate_design):
        mock_generate_design.return_value = {
            "furniture": [
                {"name": "Test Chair", "category": "chair", "price_estimate": "$100"}
            ],
            "color_scheme": ["white", "gray"],
            "placement_tips": "Place near the window.",
        }

        self.login_seed_user()

        data = {
            "style_theme": "Modern",
            "room_image": (io.BytesIO(b"\xff\xd8\xff\xd9"), "room.jpg"),
        }
        response = self.client.post(
            "/upload",
            data=data,
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIsNotNone(payload)
        self.assertIn("furniture", payload)

    @patch("app.buddy_respond")
    def test_buddy_endpoint(self, mock_buddy_respond):
        mock_buddy_respond.return_value = {
            "text": "Here are some suggestions.",
            "audio_url": "/static/audio/mock.mp3",
        }

        self.login_seed_user()

        response = self.client.post(
            "/buddy",
            json={"message": "Suggest a sofa", "language": "en"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIsNotNone(payload)
        self.assertIn("text", payload)


if __name__ == "__main__":
    unittest.main()
