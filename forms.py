__author__ = "Ken W. Alger, David Dinkins, Dan Johnson, Keri Nicole"
__copyright__ = "Copyright 2015, ZyzzyxTech"
__credits__ = ["Ken W. Alger, Dan Johnson, David Dinkins, Keri Nicole"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Ken W. Alger"
__email__ = "ken@kenwalger.com"
__status__ = "Development"


from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)

from models import User


def name_exists(form, field):
    """Checks to see if the user name already exists."""
    if User.select().where(User.th_user_name == field.data).exists():
        raise ValidationError('Sorry, that Treehouse student is already in our system.')


def email_exists(form, field):
    """Checks to see if the email has already exists."""
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('Sorry, that email address is already in our system.')


class RegisterForm(Form):
    """Creates the site registration form fields and validators"""
    # TODO: Form registration needs to validate Treehouse username, email, and password.
    # TODO: Registration form includes github address, city, state, and country.
    pass


class LoginForm(Form):
    """The form for logging into the site"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])