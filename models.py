from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password_hash = db.Column(db.String(255), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	designs = db.relationship("Design", back_populates="user", lazy=True)
	bookings = db.relationship("Booking", back_populates="user", lazy=True)

	def set_password(self, password: str) -> None:
		self.password_hash = generate_password_hash(password)

	def check_password(self, password: str) -> bool:
		return check_password_hash(self.password_hash, password)


class Design(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	image_path = db.Column(db.String(255), nullable=False)
	style_theme = db.Column(db.String(100), nullable=False)
	ai_output = db.Column(db.Text, nullable=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	user = db.relationship("User", back_populates="designs")


class Furniture(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	category = db.Column(db.String(80), nullable=False)
	price = db.Column(db.Float, nullable=False)
	image_url = db.Column(db.String(255), nullable=True)
	description = db.Column(db.Text, nullable=True)

	bookings = db.relationship("Booking", back_populates="furniture", lazy=True)


class Booking(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	furniture_id = db.Column(db.Integer, db.ForeignKey("furniture.id"), nullable=False)
	# 'pending' | 'confirmed' | 'cancelled'
	status = db.Column(db.String(30), default="pending", nullable=False)
	booking_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	user = db.relationship("User", back_populates="bookings")
	furniture = db.relationship("Furniture", back_populates="bookings")


class Cart(db.Model):
	id           = db.Column(db.Integer, primary_key=True)
	user_id      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	furniture_id = db.Column(db.Integer, db.ForeignKey('furniture.id'), nullable=False)
	quantity     = db.Column(db.Integer, default=1)
	furniture    = db.relationship('Furniture')


class Order(db.Model):
	id           = db.Column(db.Integer, primary_key=True)
	user_id      = db.Column(db.Integer, nullable=False)
	total_amount = db.Column(db.Integer, nullable=False)
	status       = db.Column(db.String(50), default='placed')
	created_at   = db.Column(db.DateTime, default=db.func.now())


class OrderItem(db.Model):
	id           = db.Column(db.Integer, primary_key=True)
	order_id     = db.Column(db.Integer, nullable=False)
	furniture_id = db.Column(db.Integer, nullable=False)
	quantity     = db.Column(db.Integer, default=1)
	price        = db.Column(db.Integer)


def init_db(app) -> None:
	db.init_app(app)
	with app.app_context():
		db.create_all()
