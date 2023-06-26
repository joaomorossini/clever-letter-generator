from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo
from models import User


class SignupForm(FlaskForm):
    email = StringField(validators=[
                           InputRequired(), Email(), Length(min=4, max=50)], render_kw={"placeholder": "Email *"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Password *"})

    submit = SubmitField('Signup')

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(
            email=email.data).first()
        if existing_user_email:
            flash('That e-mail account has already been used', 'warning')
            raise ValidationError('That user e-mail already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Email *"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Password *"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
