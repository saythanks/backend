from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from backend.config import Config
from backend.errors import bp as error_bp
from backend.persistence import db, redis
from backend.services.payments import bp as payments_bp
from backend.services.tracker import bp as tracker_bp
from backend.services.health import bp as health_bp
from backend.util import firebase, rollbar

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
    migrate.init_app(app, db.db)
    redis.init_app(app)

    # Rollbar is a logging service which automatially captures and analyzes any error we throw
    rollbar.init_app(app)

    ###########################
    # Register our blueprints #
    ###########################

    app.register_blueprint(error_bp)  # No actual routes, just error handling
    app.register_blueprint(payments_bp)
    app.register_blueprint(tracker_bp)
    app.register_blueprint(health_bp)

    return app


# Make sure our models are in scope
from backend import model

# Elastic beanstalk needs a variabled named 'applicaton' ugh
application = create_app()
