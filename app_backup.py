# External dependencies
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

# Internal dependencies
from config import DevelopmentConfig, ProductionConfig

# Instantiating Flask class
app = Flask(__name__)

# Set the configuration based on the environment
if os.getenv('FLASK_ENV') == 'development':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)

# Creating database
db = SQLAlchemy(app)

# Instantiating Bcrypt
bcrypt = Bcrypt(app)

# Flask Mail
mail = Mail(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Importing routes at the end to avoid circular imports
from routes import *
from models import *
from forms import *

# Create tables if they do not exist
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run()
