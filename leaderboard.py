"""This will create the Treehouse Leaderboard Application"""

__author__ = "Ken W. Alger, David Dinkins, Dan Johnson, Keri Nicole"
__copyright__ = "Copyright 2015, ZyzzyxTech"
__credits__ = ["Ken W. Alger, Dan Johnson, David Dinkins, Keri Nicole"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Ken W. Alger"
__email__ = "ken@kenwalger.com"
__status__ = "Development"

from flask import (Flask, g, render_template, flash, redirect, url_for,
                   abort)
from flask.ext.bcypt import check_password_hash
from flask.ext.login import (LoginManager, login_user, logout_user,
                             login_required, current_user)

import models

# Set the Debug Mode
DEBUG = True

# HTTP port on which the app will run
PORT = 8000

# Externally visable server IP address
HOST = '0.0.0.0'

# Create an instance of the Flask class
app = Flask(__name__)

# set the secret key. keep this really secret...
app.secret_key = 'k{rz`QiDW8kr9bR8]zv8k]D\P~hx,DkpX%BXYP=[@9^YWN{iV~,\XU$hF;<Cf*'

'''
----------------------------------------
Application Management
----------------------------------------
'''


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


'''
----------------------------------------
Application Routes
----------------------------------------
'''


@app.route('/')
def hello_world():
    return 'Welcome to the Flask based Treehouse Leaderboard Site'


'''
----------------------------------------
Run the application
----------------------------------------
'''


if __name__ == '__main__':
    app.run()
