
"""
Handles the database related functions for the application.
Note that we are using PostgresqlExtDatabase as opposed to
peewee.PostgresqlDatabase.
"""

__author__ = "Ken W. Alger, David Dinkins, Dan Johnson, Keri Nicole"
__copyright__ = "Copyright 2015, ZyzzyxTech"
__credits__ = ["David Dinkins, Ken W. Alger, Dan Johnson, Keri Nicole"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Ken W. Alger"
__email__ = "ken@kenwalger.com"
__status__ = "Development"

import datetime

from bcrypt import gensalt
from bcrypt import hashpw
from flask.ext.login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from peewee import *
from playhouse.postgres_ext import JSONField

import config

DATABASE = config.DATABASE
CHARACTER_ENCODING = config.CHARACTER_ENCODING
ROUNDS = config.ROUNDS
SECRET_KEY = config.SECRET_KEY


class BaseModel(Model):
    """
    A base model that will use our Postgresql database.
    """
    class Meta:
        database = config.DATABASE


class Student(UserMixin, BaseModel):
    """T
    he student model which includes:
    Treehouse Username
    Treehouse User JSON data
    Email address
    Password
    GitHub link
    City, State, & Country
    Joined at date & time
    Admin setting
    """
    th_username = CharField(unique=True)
    th_user_json_data = JSONField()
    email = CharField(unique=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    password = CharField(max_length=100)
    github_username = CharField(max_length=255)
    city = CharField(max_length=100)
    state = CharField(max_length=50)
    country = CharField(max_length=25)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        order_by = ('-joined_at',)

    @classmethod
    def create_student(cls, username, user_json, email, first_name, last_name, password, github_username, city,
                    state, country, admin=False):
        """
        Generate the student table in the database.

        Args:
            username: the student's Treehouse username (Unique)
            user_json: the student's Treehouse badge/point report in JSON format
            email: the student's email address (Unique)
            first_name: the student's first name
            last_name: the student's last name
            password: the student's password, stored as a bcrypt hash
            github_username: the student's username for github.com
            city: the student's city of residence
            state: the student's state of residence
            country: the student's country of residence
            admin: is the student a site administrator

        Raises:
            ValueError: if student is already registered in the system.
        """
        # TODO: Generate JSON data prior to storage of user profile data.
        try:
            with DATABASE.transaction():
                cls.create(
                    th_username=username,
                    th_user_json_data=user_json,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=hashpw(password.encode(CHARACTER_ENCODING), gensalt(ROUNDS)),
                    github_username=github_username,
                    city=city,
                    state=state,
                    country=country,
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("Sorry, user already exists.")

    def get_token(self, expiration=1800):
        """
        Encode a secure token

        Args:
            expiration: the time in seconds the token will live
        Returns:
            token: the generated token
        """
        s = Serializer(SECRET_KEY, expiration)
        return s.dumps({'student': self.id}).decode(CHARACTER_ENCODING)

    @staticmethod
    def verify_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except:
            return None
        id = data.get('student')
        if id:
            return Student.query.get(id)
        return None


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Student], safe=True)
    DATABASE.close()