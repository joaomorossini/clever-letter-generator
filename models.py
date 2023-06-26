from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from time import time
from datetime import datetime
from app import app

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    # ... same as before ...

class Log(db.Model):
    # ... same as before ...
