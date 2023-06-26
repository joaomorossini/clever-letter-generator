# External dependencies
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import jwt
from time import time
from datetime import datetime
# Internal dependencies
from app import app

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    api_key = db.Column(db.String(200))
    cv = db.Column(db.String(5000), default='')

    def get_reset_token(self, expires_sec=1800):
        payload = {
            'user_id': self.id,
            'exp': time() + expires_sec
        }
        return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_token(token):
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        return User.query.get(user_id)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    job_title = db.Column(db.String(100), nullable=False)
    employer_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Log('{self.timestamp}', '{self.employer_name}', '{self.job_title}')"
