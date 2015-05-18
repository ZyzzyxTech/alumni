"""
Leaderboard application configuration values
"""

__author__ = 'Ken'

from playhouse.postgres_ext import PostgresqlExtDatabase

"""
Constants for application configuration
"""

DEBUG = True
HTTP_PORT = 8000
HOST_IP = '0.0.0.0'


"""
Database Configuration Statement

Args:
    database: database name on the server
    user: user name for database access
    password: password associated with the user name
"""
DATABASE = PostgresqlExtDatabase(database='leaderboard', user='postgres')

# Application Secret Key
SECRET_KEY = 'k{rz`QiDW8kr9bR8]zv8k]D\P~hx,DkpX%BX3adf32wexP=[@9^YWN{iV~,\XU$hF;<Cf*'

# Number of password hash rounds, set low for development, increase for production
ROUNDS = 5

# Encoding format for password hashing.
CHARACTER_ENCODING = 'UTF-8'

"""
Mail Server Set-up
"""

MAIL_SERVER = 'smtp.someserver.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'
