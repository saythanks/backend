import os
from flask import Flask
from flask_cors import CORS
# from payments import bp as payments_bp
import backend.payments as payments
# from flask.ext.redis import FlaskRedis

# redis_store = FlaskRedis()

# Flask server Application Factory

balance = 10

def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        # DB setup would also happen here
    )

    # redis_store.init_app(app)
    

    if test_config is None:
        # load the instance config (config.py) if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the provided test config if passed into create_app
        app.config.from_mapping(test_config)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register blueprints with app
    app.register_blueprint(payments.bp)

    return app


# Elastic beanstalk needs a variabled named 'applicaton' ugh
application = create_app()
