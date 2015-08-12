"""
This will create the Treehouse Leaderboard Application
"""

__author__ = "Ken W. Alger, David Dinkins, Dan Johnson, Keri Nicole"
__copyright__ = "Copyright 2015, ZyzzyxTech"
__credits__ = ["David Dinkins, Ken W. Alger, Dan Johnson, Keri Nicole"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Ken W. Alger"
__email__ = "ken@kenwalger.com"
__status__ = "Development"

from bcrypt import hashpw
from flask import (Flask, g, render_template, flash, redirect, url_for, abort)
from flask.ext.login import (LoginManager, login_user, logout_user,
                             login_required, current_user)
from flask_mail import Mail, Message

from assets import assets
from security import generate_confirmation_token, confirm_token
from models import Student

import datetime

import config
import data_requests
import forms
import models



# Statement for enabling the development environment
DEBUG = config.DEBUG

# HTTP port on which the app will run
PORT = config.HTTP_PORT

# Externally visible server IP address
HOST = config.HOST_IP

# Create an instance of the Flask class
app = Flask(__name__)
# Register mail server configuration
mail = Mail(app)
# Initialize assets for CSS and JavaScript
assets.init_app(app)


# set the secret key. keep this really secret...
app.secret_key = config.SECRET_KEY

# Mail Server Settings
app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD

# Login Manager Settings

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


"""
Application Management
"""


@login_manager.user_loader
def load_student(student_id):
    try:
        return models.Student.get(models.Student.id == student_id)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """
    Connect to the database before each request.
    """
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """
    Close the database connection after each request.
    """
    g.db.close()
    return response


"""
Application View Routes
"""


@app.route('/')
def index():
    """
    Application landing page.
    Display top 25 registered Treehouse students from the database.
    """
    # TODO: setup landing page, index.html
    stream = models.Student.select().limit(25)
    return render_template('index.html', stream=stream, title="Home")


@app.route('/register', methods=('GET', 'POST'))
def register():
    """
    User registration page
    """
    form = forms.StudentRegisterForm()
    if form.validate_on_submit():
        flash("Yippie, you have joined the Treehouse Alumni Site!", "success")
        models.Student.create_student(
            username=form.th_username.data,
            user_json=data_requests.request_user_data(form.th_username.data),
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data,
            github_username=form.github.data,
            city=form.city.data,
            state=form.state.data,
            country=form.country.data
        )

        # Now we'll send the email confirmation link
        subject = "Confirm your email"

        token = generate_confirmation_token(form.email.data)

        return redirect(url_for('index'))
    return render_template('register.html', form=form, title='Register')

@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    student = Student.query.filter_by(email=email).first_or_404()
    if student.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        student.confirmed = True
        student.confirmed_on = datetime.datetime.now()
        models.Student.update(student)


@app.route('/login', methods=('GET', 'POST'))
def login():
    """
    Login to site page
    """
    # TODO: Fix user login password check
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            student = models.Student.get(models.Student.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if student.password == hashpw(form.password.data.encode('UTF_8'),
                                          student.password.encode('UTF-8')).decode():
                login_user(student)
                flash("You've been logged in!", "success")
                return redirect(url_for('leaderboard'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form, title='Login')


@app.route('/about', methods=('GET', 'POST'))
def about():
    """
    About page
    """
    return render_template('about.html', title='About Us')


@app.route('/legal', methods=('GET', 'POST'))
def legal():
    """
    Legal disclaimer
    """
    return render_template('legal.html', title='Legal')


"""
Application View Routes :: Login Required
"""

@app.route('/logout')
@login_required
def logout():
    """
    Logout from application page
    """
    logout_user()
    flash("Thanks for visiting, you are now logged out. Please come back soon!", "success")
    return redirect(url_for('index'))


@app.route('/update')
@login_required
def update():
    """
    Update the current user's profile
    """
    form = forms.UpdateProfile()
    # TODO: update student information
    return render_template('update-profile.html', form=form, title='Profile Update')


@app.route('/leaderboard')
@login_required
def leaderboard(username=None):
    """
    Display the current leaderboard.
    """
    # TODO: setup leaderboard page, leaderboard.html
    template = 'leaderboard.html'
    if username and username != current_user.username:
        try:
            student = models.Student.select.where(
                models.Student.th_username**username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            stream = models.Student.select().limit(25)
    return render_template('leaderboard.html', title='Students')

"""
Application View Routes :: Password Reset
"""

@app.route('/reset-password', methods=('GET', 'POST'))
def forgot_password():
    """
    Route to reset a student's password.
    """
    form = forms.ResetPassword()
    # TODO: Handle token creation for password reset
    # token = request.args.get('token', None)
    # form = forms.ResetPassword(request.form)
    # if form.validate_on_submit():
    #     email = form.email.data
    #     student = student.query.filter_by(email=email).first()
    #     if student:
    #         token = student.get_token()
    #         print token
    return render_template('reset.html', form=form, title='Reset Password')

"""
Application View Routes :: HTTP Error handling
"""

@app.errorhandler(403)
def forbidden(error):
    """
    Handles HTTP 403 error conditions.
    """
    return render_template('403.html', title="403 Error"), 403


@app.errorhandler(404)
def not_found(error):
    """
    Handles HTTP 404 error conditions.
    """
    return render_template('404.html', title="404 Error"), 404


@app.errorhandler(418)
def tea_pot(error):
    """
    Handles HTTP 418 error conditions.

    I'm a little teapot, short and stout...
    """
    return render_template('418.html', title="418 Error"), 418


@app.errorhandler(500)
def server_error(error):
    """
    Handles HTTP 500 error conditions.
    """
    return render_template('500.html', title="500 Error"), 500

"""
Run the application
"""


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
