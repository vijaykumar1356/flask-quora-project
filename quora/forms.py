from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.validators import ValidationError
from quora.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=20,
               message="Name should be atleast 3 characters in length!")
                ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password',
                message="Password should match with Confirm Password Field!")
                ])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """
        To check if username already exists in db while registering!
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                    'That username already exists! Try different.')

    def validate_email(self, email):
        """
        to check if email already exists in db while registering!
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                    'That email already registered! try a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class AskQuestion(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    submit = SubmitField('Ask Question!')


class AnswerForm(FlaskForm):
    content = TextAreaField('Answer', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
                DataRequired(),
                Length(
                    min=3, max=20,
                    message="Name should be atleast 3 characters in length!")
                    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

# This class requires argument original_username which comes from routes.py
    def __init__(self, original_username, original_email, *args,  **kwargs):
        super(UpdateAccountForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        """
        while updating user data, it first checks username with old username
        of user and then checks further for any user who has same username
        """
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError(
                    'That username already exists! try a different one.'
                    )

    def validate_email(self, email):
        """
        while updating user data, it first checks email with old email
        of user and then checks further for any user who has same email
        """
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError(
                    'That email already registered! try a different one.'
                    )
