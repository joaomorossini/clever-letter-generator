from models import *

# Development
# prompt_template = f"""Generate a one paragraph long cover letter
# based on the info delimited by double angle brackets.
# <<cv: {cv} | job title: {job_title} | job description: {job_description}
# employer name: {employer_name} | employer description: {employer_description}
# additional instructions: {additional_instructions}>>"""

# Production
prompt_template = """Based on the info below, delimited by angle brackets, create a professional
cover letter, which should be structured as follows:

Paragraph 1: Greeting and introduction. Try to be a little creative here
in order to get the hiring manager's attention in a positive way.

Paragraphs 2 to 4: Explain in a persuasive but honest manner why I'm a good fit
for the job. Whenever possible, link my skills, experiences, education and personality
traits to the job requirements, both "must haves" and "good to haves".

Final Paragraph: Show appreciation to the reader for taking the time to review
my application. Demonstrate in an honest tone my interest and motivation to
further explore the ways in which I could be of value to the employer.

Each paragraph should be followed by a newline (\n) and the last one should be followed by two newlines (\n\n).

Finish with 'Sincerely,'

CV: <{cv}> | Employer Name: <{employer_name}> | Employer description: <{employer_description}
Job Title: <{job_title}> | Job Description: <{job_description}> | Additional Instructions: <{additional_instructions}>"""