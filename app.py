"""This will create the Treehouse Leaderboard Application"""

__author__ = "Ken W. Alger, David Dinkins, Dan Johnson, Keri Nicole"
__copyright__ = "Copyright 2015, ZyzzyxTech"
__credits__ = ["Ken W. Alger, Dan Johnson, David Dinkins, Keri Nicole"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Ken W. Alger"
__email__ = "ken@kenwalger.com"
__status__ = "Development"

from flask import (Flask, g, render_template, flash, redirect, url_for, abort)
from flask.ext.login import (LoginManager, logout_user,
                             login_required, current_user)

import data_requests
import forms
import models




# Set the Debug Mode
DEBUG = True

# HTTP port on which the app will run
PORT = 8000

# Externally visible server IP address
HOST = '0.0.0.0'

# Create an instance of the Flask class
app = Flask(__name__)

# set the secret key. keep this really secret...
app.secret_key = 'k{rz`QiDW8kr9bR8]zv8k]D\P~hx,DkpX%BXYP=[@9^YWN{iV~,\XU$hF;<Cf*'

# Login Manager Settings

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# ----------------------------------------
# Application Management
# ----------------------------------------


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


# ----------------------------------------
# Application Routes
# ----------------------------------------


@app.route('/')
def index():
    """Application landing page.
    Display top 25 registered Treehouse students from the database.
    """
    # TODO: setup landing page, index.html
    stream = models.Student.select().limit(25)
    return render_template('index.html', stream=stream)


@app.route('/register', methods=('GET', 'POST'))
def register():
    """User registration page"""
    form = forms.StudentRegisterForm()
    if form.validate_on_submit():
        flash("Yippie, you have joined the Treehouse Alumni Site!", "success")
        models.Student.create_student(
            username=form.th_username.data,
            user_json=data_requests.request_user_data(form.th_username.data),
            email=form.email.data,
            password=form.password.data,
            github_account_link=form.github.data,
            city=form.city.data,
            state=form.state.data,
            country=form.country.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    """Login to site page"""
    form = forms.LoginForm()
    # TODO: setup login page, login.html
    return render_template('login.html', form=form)


@app.route('/about', methods=('GET', 'POST'))
def about():
    """About page"""
    return render_template('about.html')


@app.route('/legal', methods=('GET', 'POST'))
def legal():
    """Legal disclaimer"""
    return render_template('legal.html')


# ----------------------------------------
# Login required routes
# ----------------------------------------

@app.route('/logout')
@login_required
def logout():
    """Logout from application page"""
    logout_user()
    flash("Thanks for visiting, you are now logged out. Please come back soon!", "success")
    return redirect(url_for('index'))


@app.route('/leaderboard')
@login_required
def leaderboard(username=None):
    """Display the current leaderboard"""
    # TODO: setup leaderboard page, leaderboard.html
    template = 'leaderboard.html'
    if username and username != current_user.username:
        try:
            user = models.User.select.where(
                models.User.th_username**username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            stream = user.leaders.limit(100)
    return render_template('leaderboard.html')


# ----------------------------------------
# Routes for HTML error handling
# ----------------------------------------

@app.errorhandler(403)
def forbidden(error):
    """Handles HTML 403 error conditions."""
    return render_template('403.html'), 403


@app.errorhandler(404)
def not_found(error):
    """Handles HTML 404 error conditions."""
    return render_template('404.html'), 404


@app.errorhandler(418)
def tea_pot(error):
    """Handles HTML 418 error conditions.
    I'm a little teapot, short and stout..."""
    return render_template('418.html'), 418


@app.errorhandler(500)
def server_error(error):
    """Handles HTML 500 error donditions."""
    return render_template('500.html'), 500

# ----------------------------------------
# Run the application, create initial
# sample user
# ----------------------------------------


if __name__ == '__main__':
    models.initialize()
    try:
        models.Student.create_student(
            username='kenalger',
            user_json=data_requests.request_user_data('kenalger'),
            email='ken@kenwalger.com',
            password='password',
            github_account_link='https://github.com/kenwalger',
            city='Portland',
            state='OR',
            country='USA',
            admin=True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
