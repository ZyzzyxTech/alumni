
"""Handles the database related functions for the application.
    Note that we are using PostgresqlExtDatabase as opposed to
    the usual peewee.PostgresqlDatabase.
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
from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase, JSONField

DATABASE = PostgresqlExtDatabase(database='leaderboard', user='postgres')
ROUNDS = 5     # Number of hash rounds, set low for development, increase for production


class BaseModel(Model):
    """A base model that will use our Postgresql database."""
    class Meta:
        database = DATABASE


class Student(UserMixin, BaseModel):
    """The student model which includes:
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
        """Generate the student table in the database."""
        # TODO: Generate JSON data prior to storage of user profile data.
        try:
            with DATABASE.transaction():
                cls.create(
                    th_username=username,
                    th_user_json_data=user_json,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=hashpw(password.encode('UTF-8'), gensalt(ROUNDS)),
                    github_username=github_username,
                    city=city,
                    state=state,
                    country=country,
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("Sorry, user already exists.")


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Student], safe=True)
    DATABASE.close()