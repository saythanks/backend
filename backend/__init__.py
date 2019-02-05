import os
from flask import Flask, got_request_exception
from flask_cors import CORS


from backend.config import Config

from backend.payments import bp as payments_bp
from backend.error import bp as error_bp

from backend.persistence.database import init_db
from backend.persistence.redis import init_redis

from backend.util.rollbar import init_rollbar


# Flask server Application Factory


balance = 0


def include_config(app, test_config):
    # Inlcude our config file
    app.config.from_object(Config)

    if test_config is None:
        # load the instance config (config.py) if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the provided test config if passed into create_app
        app.config.from_mapping(test_config)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    include_config(app, test_config)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Ugh cors
    CORS(app)

    # Init necessary dependencies with our current app
    init_db(app)
    init_redis(app)

    # Rollbar is a logging service which automatially captures and analyzes any error we throw
    init_rollbar(app)

    ###########################
    # Register our blueprints #
    ###########################
    app.register_blueprint(payments_bp)
    app.register_blueprint(error_bp)

    return app


# Elastic beanstalk needs a variabled named 'applicaton' ugh
application = create_app()
