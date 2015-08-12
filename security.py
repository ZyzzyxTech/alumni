__author__ = 'Ken'

from itsdangerous import URLSafeTimedSerializer

import config


def generate_confirmation_token(email):
    timedserializer = URLSafeTimedSerializer(config.SECRET_KEY)
    return timedserializer.dumps(email, salt=config.SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=config.DEFAULT_EXPIRATION):
    timedserializer = URLSafeTimedSerializer(config.SECRET_KEY)
    try:
        email = timedserializer.loads(
            token,
            salt=config.SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email


