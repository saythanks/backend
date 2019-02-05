import os
from flask import Flask, got_request_exception
from flask_cors import CORS
from flask_migrate import Migrate

from backend.config import Config

from backend.payments import bp as payments_bp
from backend.errors import bp as error_bp

from backend.persistence import redis, db
from backend.util import rollbar


# Setup the globals we need
migrate = Migrate()

# Flask server Application Factory


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    if test_config is not None:
        # load the provided test config if passed into create_app
        app.config.from_mapping(test_config)

    # Ugh cors
    CORS(app)

    # Init necessary dependencies with our current app
    db.init_app(app)
    migrate.init_app(app, db)
    redis.init_app(app)
    rollbar.init_app(app)

    # Rollbar is a logging service which automatially captures and analyzes any error we throw

    ###########################
    # Register our blueprints #
    ###########################
    app.register_blueprint(payments_bp)
    app.register_blueprint(error_bp)

    from backend.services.tracker import bp as tracker_bp
    app.register_blueprint(tracker_bp)

    return app


from backend import model

# Elastic beanstalk needs a variabled named 'applicaton' ugh
application = create_app()
