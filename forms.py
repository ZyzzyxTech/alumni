"""Handles the form data for the application"""

__author__ = "Ken W. Alger, David Dinkins, Dan Johnson, Keri Nicole"
__copyright__ = "Copyright 2015, ZyzzyxTech"
__credits__ = ["Ken W. Alger, Dan Johnson, David Dinkins, Keri Nicole"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Ken W. Alger"
__email__ = "ken@kenwalger.com"
__status__ = "Development"


from flask_wtf import Form
from flask_wtf.html5 import URLField
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)

from models import Student


def name_exists(form, field):
    """Checks to see if the user name already exists."""
    if Student.select().where(Student.th_user_name == field.data).exists():
        raise ValidationError('Sorry, that Treehouse student is already in our system.')


def email_exists(form, field):
    """Checks to see if the email has already exists."""
    if Student.select().where(Student.email == field.data).exists():
        raise ValidationError('Sorry, that email address is already in our system.')


class StudentRegisterForm(Form):
    """Creates the site registration form fields and validators"""
    # TODO: Form registration needs to validate Treehouse username, email, and password.
    # TODO: Registration form includes github URL, city, state, and country.
    th_username = StringField(
        'Treehouse Username',
        validators=[
            DataRequired(),
            name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    github = StringField(
        'Github URL',
        validators=[
            URLField()
        ])
    city = StringField(
        'City'
    )
    state = StringField(
        'State'
    )
    country = StringField(
        'Country',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Passord',
        validators=[DataRequired()]
    )


class LoginForm(Form):
    """The form for logging into the site"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])