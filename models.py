__author__ = 'Ken W. Alger'

import datetime

from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('student.db')

class User(UserMixin, Model):
    th_user_name = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    github_account_link = CharField(max_length=255)
    city = CharField(max_length=100)
    state = CharField(max_length=50)
    country = CharField(max_length=25)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at', '-th_user_name')


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()