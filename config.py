__author__ = 'Ken'

from playhouse.postgres_ext import PostgresqlExtDatabase

"""
Constants for application configuration
"""

DEBUG = True
HTTP_PORT = 8000
HOST_IP = '0.0.0.0'

CHARACTER_ENCODING = 'UTF-8'
DATABASE = PostgresqlExtDatabase(database='leaderboard', user='postgres')
SECRET_KEY = 'k{rz`QiDW8kr9bR8]zv8k]D\P~hx,DkpX%BX3adf32wexP=[@9^YWN{iV~,\XU$hF;<Cf*'
ROUNDS = 5     # Number of hash rounds, set low for development, increase for production

"""
Mail Server Set-up
"""

MAIL_SERVER = 'smtp.someserver.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'
