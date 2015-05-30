__author__ = 'Ken'

from itsdangerous import URLSafeTimedSerializer

from app import app
import config

def generate_confirmation_token(email):
    timedserializer = URLSafeTimedSerializer(app.config[config.SECRET_KEY])
    return timedserializer.dumps(email, salt=app.config[config.SECURITY_PASSWORD_SALT])

def confirm_token(token, expiration=config.DEFAULT_EXPIRATION):
    timedserializer = URLSafeTimedSerializer(app.config[config.SECRET_KEY])
    try:
        email = timedserializer.loads(
            token,
            salt=app.config[config.SECURITY_PASSWORD_SALT],
            max_age=expiration
        )
    except:
        return False
    return email