# External dependencies
import os
import openai
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request
from flask import Flask, render_template, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from flask_wtf import FlaskForm
# from flask_bcrypt import Bcrypt
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Length, ValidationError

# Internal dependencies
from prompt_template import prompt_template


app = Flask(__name__)  # Instantiating Flask class
# db = SQLAlchemy(app)  # Creating database
# bcrypt = Bcrypt(app)  # ???
#---------!VERIFICAR!----------#
#PESQUISAR O QUE É SECRETKEY E COMO USAR ADEQUADAMENTE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'


#----------------AUTHENTICATION - START----------------#
# Initializing LoginManager
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
#
#
# class User(db.model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)

#----------------AUTHENTICATION - END----------------#


# Setting up environment
_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.getenv('OPENAI_API_KEY')


# Defining the helper function
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


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


if __name__ == '__name__':
    app.run(debug=True)
