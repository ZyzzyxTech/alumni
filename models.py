__author__ = "Ken W. Alger, David Dinkins, Dan Johnson,  Keri Nicole"
__copyright__ = "Copyright 2015, ZyzzyxTech"
__credits__ = ["Ken W. Alger, Dan Johnson, David Dinkins, Keri Nicole"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Ken W. Alger"
__email__ = "ken@kenwalger.com"
__status__ = "Development"

import datetime

from flask.ext.login import UserMixin
from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase, JSONField

DATABASE = PostgresqlExtDatabase('leaderboard.db', user="postgres")

class BaseModel(Model):
    """A base model that will use our Postgresql database."""
    class Meta:
        database = DATABASE
        order_by = ('-joined_at', '-th_user_name')

class User(UserMixin, BaseModel):
    th_user_name = CharField(unique=True)
    th_user_json_data = JSONField()
    email = CharField(unique=True)
    password = CharField(max_length=100)
    github_account_link = CharField(max_length=255)
    city = CharField(max_length=100)
    state = CharField(max_length=50)
    country = CharField(max_length=25)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()