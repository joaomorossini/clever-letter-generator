import os
from dotenv import load_dotenv, find_dotenv

# Setting up environment
_ = load_dotenv(find_dotenv())  # read local .env file

class Config(object):
    # Defining the path to the database
    root_folder = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(root_folder, 'instance', 'database.db')

    # Configuring the database
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{database_path}"  # Connecting app to the database
    SECRET_KEY = os.getenv('SECRET_KEY', 'thisisasecretkey')
    MAIL_SERVER = 'smtp.googlemail.com'  # or your preferred SMTP server
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False