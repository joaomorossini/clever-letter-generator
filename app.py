# Importing external dependencies
import os
import openai
from flask import Flask, render_template, request
from dotenv import load_dotenv, find_dotenv
from prompt_template import prompt_template

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
@app.route('/', methods=['GET', 'POST'])
def home():
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
    return render_template('index.html', response=response)


if __name__ == '__name__':
    app.run()
