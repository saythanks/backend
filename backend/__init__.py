from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from backend.config import Config
from backend.errors import bp as error_bp
from backend.persistence import db, redis


from backend.services.payments import bp as payments_bp
from backend.services.tracker import bp as tracker_bp
from backend.services.health import bp as health_bp
from backend.services.apps import bp as apps_bp

from backend.util import rollbar
from backend.util.marshmallow import ma

from backend.model.model import BaseModel

# Setup the globals we need
migrate = Migrate()


# Flask server Application Factory


from flask import jsonify, Response


def to_dict(val):
    if isinstance(val, BaseModel):
        return val.to_dict()

    return val


def to_json(val):
    if isinstance(val, dict):
        return jsonify(val)

    elif isinstance(val, list):
        return jsonify(list(map(lambda v: to_dict(v), val)))

    elif isinstance(val, BaseModel):
        return jsonify(val.to_dict())

    return val


class JSONResponse(Response):

    default_mimetype = "application/json"

    @classmethod
    def force_type(cls, rv, environ=None):
        # if isinstance(rv, list):
        #     rv = jsonify(list(map(lambda v: to_dict(v), rv)))
        # else:
        #     rv = jsonify(to_dict(rv))

        rv = to_json(rv)

        return super(JSONResponse, cls).force_type(rv, environ)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    app.response_class = JSONResponse

    if test_config is not None:
        # load the provided test config if passed into create_app
        app.config.from_mapping(test_config)

    # Ugh cors
    CORS(app)

    # Init necessary dependencies with our current app
    db.init_app(app)
    migrate.init_app(app, db.db)
    redis.init_app(app)
    ma.init_app(app)

    # Rollbar is a logging service which automatially captures and analyzes any error we throw
    rollbar.init_app(app)

    ###########################
    # Register our blueprints #
    ###########################

    app.register_blueprint(error_bp)  # No actual routes, just error handling
    app.register_blueprint(payments_bp)
    app.register_blueprint(tracker_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(apps_bp)

    return app


# Make sure our models are in scope
from backend import model

# Elastic beanstalk needs a variabled named 'applicaton' ugh
application = create_app()
