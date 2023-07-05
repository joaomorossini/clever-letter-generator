# External dependencies
import os
import re
from dotenv import load_dotenv, find_dotenv

# Setting up environment
_ = load_dotenv(find_dotenv())  # read local .env file

# Creating Config class
class Config(object):
    # Defining the path to the database
    root_folder = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(root_folder, 'instance', 'database.db')

    # Database
    DATABASE_URL = os.getenv('DATABASE_URL')  # Connecting app to the database
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL

    SECRET_KEY = os.getenv('SECRET_KEY')
    # Mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')
    # API
    OPENAI_API_KEY_DEV = os.getenv('OPENAI_API_KEY_DEV')


# Development Environment
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{Config.database_path}"


# Production Environment
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False