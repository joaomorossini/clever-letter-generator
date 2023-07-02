# External dependencies
import os
from dotenv import load_dotenv, find_dotenv

# Setting up environment
_ = load_dotenv(find_dotenv())  # read local .env file


# Creating Config class
class Config(object):
    # Defining the path to the database
    root_folder = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(root_folder, 'instance', 'database.db')

    # Database
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{database_path}"  # Connecting app to the database
    SECRET_KEY = os.getenv('SECRET_KEY', 'thisisasecretkey')
    # Mail
    MAIL_SERVER = 'smtp.googlemail.com'  # or your preferred SMTP server
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


# Production Environment
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
