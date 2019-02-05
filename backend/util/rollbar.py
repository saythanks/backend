import os

from flask import got_request_exception
import rollbar
import rollbar.contrib.flask

from backend.config import Config


def init_app(app):
    # Logging
    rollbar.init(
        # access token for the demo app: https://rollbar.com/demo
        Config.ROLLBARR_KEY,
        # environment name
        'backend',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
