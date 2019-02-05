import os


class Config(object):

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    SESSION_COOKIE_HTTPONLY = True
    PREFERRED_URL_SCHEME = 'https'

    # Connection URLS
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost')

    # API Stuff
    STRIPE_KEY = os.environ.get('STRIPE_KEY')
    STRIPE_SECRET = os.environ.get('STRIPE_SECRET')
    ROLLBARR_KEY = os.environ.get('ROLLBAR_KEY')

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'postgres://root:root@db:5432'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
