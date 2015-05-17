"""Handles the form data for the application"""

__author__ = "Ken W. Alger, David Dinkins, Dan Johnson, Keri Nicole"
__copyright__ = "Copyright 2015, ZyzzyxTech"
__credits__ = ["David Dinkins, Ken W. Alger, Dan Johnson, Keri Nicole"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Ken W. Alger"
__email__ = "ken@kenwalger.com"
__status__ = "Development"

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)

from models import Student


"""
Methods to check for uniqueness of data
"""


def student_name_exists(form, field):
    """Checks to see if the student name already exists."""
    if Student.select().where(Student.th_username == field.data).exists():
        raise ValidationError('Sorry, that Treehouse student is already in our system.')


def email_exists(form, field):
    """Checks to see if the email already exists."""
    if Student.select().where(Student.email == field.data).exists():
        raise ValidationError('Sorry, that email address is already in our system.')


"""
Registration Forms
"""


class StudentRegisterForm(Form):
    """Creates the site registration form fields and validators"""
    # TODO: Form registration needs to validate Treehouse username, email, and password.
    th_username = StringField(
        'Treehouse Username',
        validators=[
            DataRequired(),
            student_name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    first_name = StringField(
        'First Name',
        validators=[DataRequired()])
    last_name = StringField(
        'Last Name',
        validators=[DataRequired()])
    github = StringField(
        'Github Username')
    city = StringField(
        'City')
    state = StringField(
        'State')
    country = StringField(
        'Country')
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class LoginForm(Form):
    """The form for logging into the site"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class UpdateProfile(Form):
    """The form for updating profile information"""

    email = StringField(
        'Email',
        validators=[
            email_exists
        ])
    first_name = StringField(
        'First Name')
    last_name = StringField(
        'Last Name')
    github = StringField(
        'Github Username')
    city = StringField(
        'City')
    state = StringField(
        'State')
    country = StringField(
        'Country')


"""
Password Reset Forms
"""


class ExistingStudent(object):
    def __init__(self, message="Email doesn't exist"):
        self.message = message

    def __call__(self, form, field):
        if not Student.query.filter_by(email=field.data).first():
            raise ValidationError(self.message)

reset_rules = [DataRequired(),
               Email(),
               ExistingStudent(message='Email address is not available.')]


class ResetPassword(Form):
    email = StringField('Email', validators=reset_rules)


class ResetPasswordSubmit(Form):
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )
