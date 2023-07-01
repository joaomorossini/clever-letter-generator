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

# # Importing routes at the end to avoid circular imports
from routes import *


with app.app_context():
    try:
        db.create_all()
        print("Tables created.")
    except Exception as e:
        print("An error occurred while creating tables:", e)

if __name__ == '__main__':
    app.run()
