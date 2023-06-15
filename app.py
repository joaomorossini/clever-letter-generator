# ---------- DEPENDENCIES ---------- #
# External dependencies
import os
import openai
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

# Internal dependencies
from prompt_template import prompt_template


# ---------- FLASK APP AND DATABASE ---------- #
app = Flask(__name__)  # Instantiating Flask class
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Connecting app to the database
# REFACTOR: SECRET KEY SHOULDN'T BE VISIBLE IN A PRODUCTION ENVIRONMENT
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)  # Creating database


# ---------- CREATING CLASSES AND FORMS ---------- #
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
# REFACTOR: Should I name the db field only 'cv'? What are the best practices?
    stored_cv = db.Column(db.String(5000), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=40)], render_kw={"placeholder": "Password"})

    cv = StringField(validators=[
                             InputRequired(), Length(min=20, max=5000)], render_kw={"placeholder": "You cv goes here"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


# ---------- ROUTES ---------- #
# Defining routes
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('user_dashboard.html')


@app.route('/generator', methods=['GET', 'POST'])
def generator():
    response = ""
    if request.method == 'POST':
        cv = request.form.get('cv')
        job_title = request.form.get('job_title')
        job_description = request.form.get('job_description')
        employer_name = request.form.get('employer_name')
        employer_description = request.form.get('employer_description')
        additional_instructions = request.form.get('additional_instructions')
        prompt = prompt_template.format(cv=cv, job_title=job_title, job_description=job_description,
                                        employer_name=employer_name, employer_description=employer_description,
                                        additional_instructions=additional_instructions)
        response = get_completion(prompt)
    return render_template('generator.html', response=response)


# ---------- ENVIRONMENT VARIABLE API KEY ---------- #
# Setting up environment
_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.getenv('OPENAI_API_KEY')


# ---------- GPT HELPER FUNCTION ---------- #
# Defining the helper function
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


with app.app_context():
    try:
        print("Creating tables...")
        db.create_all()
        print("Tables created.")
    except Exception as e:
        print("An error occurred while creating tables:", e)


print("Current working directory:", os.getcwd())


print("SQLALCHEMY_DATABASE_URI:", app.config['SQLALCHEMY_DATABASE_URI'])


# ---------- END ---------- #
if __name__ == '__main__':
    app.run(debug=True)
