# Importing external dependencies
import os
import openai
from flask import Flask, render_template
from dotenv import load_dotenv, find_dotenv


# Instantiating Flask class
app = Flask(__name__)


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


# Defining the route for the homepage
@app.route('/')
def home():
    # --------------- START TEMPORARY CODE SNIPPET --------------- #
    # User inputs
    cv = """PMP Certified project manager with 5 years experience in large scale construction projects"""
    job_title = """Remote Tech Project Manager"""

    # Prompt
    prompt = f"""Generate a one paragraph long cover letter based on
    the info delimited by double angle brackets. <<cv: {cv} | job title: {job_title}>>"""
    # --------------- END TEMPORARY CODE SNIPPET --------------- #

    # Getting the completion response
    response = get_completion(prompt)

    return render_template('index.html', response=response)


if __name__ == '__name__':
    app.run()
