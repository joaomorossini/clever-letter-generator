from flask import render_template, request, url_for, redirect, flash, send_file, Response, session
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Log
from forms import SignupForm, LoginForm, RequestResetForm, ResetPasswordForm
from app import app, db, bcrypt, mail, login_manager
import openai

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('generator'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('generator'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'warning')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/generator', methods=['GET', 'POST'])
@login_required
def generator():
    # Check if the user's API key is set
    if not current_user.api_key:
        flash('Please set your API key before generating a cover letter.', 'warning')
        return redirect(url_for('dashboard'))

    response = ""
    job_title = ""
    job_description = ""
    employer_name = ""
    employer_description = ""
    additional_instructions = ""

    if request.method == 'POST':
        cv = current_user.cv
        job_title = request.form.get('job_title')
        job_description = request.form.get('job_description')
        employer_name = request.form.get('employer_name')
        employer_description = request.form.get('employer_description')
        additional_instructions = request.form.get('additional_instructions')

    if 'generate' in request.form:
        prompt = prompt_template.format(cv=cv, job_title=job_title, job_description=job_description,
                                        employer_name=employer_name, employer_description=employer_description,
                                        additional_instructions=additional_instructions)
        response = get_completion(prompt)

        # Save the response in the user's session
        session['response'] = response

        # Create a log entry
        log = Log(job_title=job_title, employer_name=employer_name, user_id=current_user.id)
        db.session.add(log)
        db.session.commit()

    elif 'clear' in request.form:
        job_title = ""
        job_description = ""
        employer_name = ""
        employer_description = ""
        additional_instructions = ""
        session['response'] = ""

    if 'download' in request.form:
        # Retrieve the response from the session
        response = session.get('response', '')
        if response == '':
            flash('Please generate a cover letter before downloading.', 'warning')
            return render_template('generator.html', response=response, job_title=job_title, job_description=job_description,
                           employer_name=employer_name, employer_description=employer_description,
                           additional_instructions=additional_instructions)

        str_io = io.StringIO()
        str_io.write(response)
        str_io.seek(0)
        # Check if employer_name and job_title are not None, else replace with 'Unknown'
        employer_name = employer_name if employer_name else 'Unknown Employer'
        # Format the filename
        filename = f"{employer_name} - {job_title} - {datetime.now().strftime('%Y.%m.%d')}.txt"
        return Response(
            str_io.getvalue(),
            mimetype="text/plain",
            headers={"Content-disposition":
                         f"attachment; filename={filename}"})

    return render_template('generator.html', response=response, job_title=job_title, job_description=job_description,
                           employer_name=employer_name, employer_description=employer_description,
                           additional_instructions=additional_instructions)


@app.route('/dashboard', methods=['GET', 'POST'])
@app.route('/dashboard/<toggle>', methods=['GET', 'POST'])
@login_required
def dashboard(toggle=None):
    if toggle == 'toggle_api_key_visibility':
        session['api_key_visible'] = not session.get('api_key_visible', False)

    if request.method == 'POST':
        # Handle API key form submission
        new_api_key = request.form.get('api_key')
        if new_api_key and new_api_key != '******':
            hashed_api_key = bcrypt.generate_password_hash(new_api_key).decode('utf-8')
            current_user.api_key = hashed_api_key
            flash('API key updated successfully.', 'success')

        # Handle CV form submission
        new_cv = request.form.get('cv')
        if new_cv:
            current_user.cv = new_cv

        try:
            db.session.commit()
        except Exception as e:
            # Log the error and show an error message to the user
            print(e)
            flash('An error occurred while updating your data. Please try again.', 'warning')

    # If the user's CV is empty, show a placeholder
    cv = current_user.cv if current_user.cv else "Your CV goes here"

    # Fetch the logs from the database
    page = request.args.get('page', 1, type=int)
    per_page = 10
    logs = Log.query.filter_by(user_id=current_user.id).order_by(Log.timestamp.desc()).paginate(page=page, per_page=per_page)
    # Fetch all logs for download
    all_logs = Log.query.filter_by(user_id=current_user.id).order_by(Log.timestamp.desc()).all()

    # Downloading logs
    if 'download_logs' in request.form:
        # Create a string representation of the logs
        logs_str = "\n".join(f"{log.timestamp}\t{log.job_title}\t{log.employer_name}" for log in all_logs)
        str_io = io.StringIO()
        str_io.write(logs_str)
        str_io.seek(0)
        filename = f"ai_cover_letter_log_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        return Response(
            str_io.getvalue(),
            mimetype="text/plain",
            headers={"Content-disposition":
                     f"attachment; filename={filename}"})

    if 'delete_api_key' in request.form:
        current_user.api_key = ''
        db.session.commit()
        flash('API key deleted successfully.', 'success')

    return render_template('dashboard.html', user=current_user, cv=cv, logs=logs)


@app.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    message = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            message = 'An e-mail has been sent with instructions to reset your password.'
    return render_template('reset_request.html', form=form, message=message)


@app.route('/reset_request/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if not user:
        # If the token is invalid or expired, redirect the user to the `reset_request` route.
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)


@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = User.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted.', 'success')
    return redirect(url_for('home'))


def get_completion(prompt, model="gpt-3.5-turbo"):
    # Check the current environment
    if app.config['DEBUG']:
        # Use your own API key for development
        api_key = app.config['OPENAI_API_KEY']
    else:
        # Use the user's API key for production
        api_key = current_user.api_key

    # Set the API key for this request
    openai.api_key = api_key

    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
