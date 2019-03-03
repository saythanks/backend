from webargs import fields
from webargs.flaskparser import use_args
from flask import jsonify

from backend.services.apps import bp
from backend.middleware.token_auth import authorized
from backend.model.app import App
from backend.model.payable import Payable
from backend.persistence.db import db
from backend.errors.ApiException import ApiException


@bp.route("/apps/<id>/payables", methods=["GET"])
@authorized
def list_payables(user, id):
    app = App.query.get(id)
    return app.payables


@bp.route("/payables/<id>", methods=["GET"])
def get_payable(user, id):
    payable = Payables.query.get(id)
    return payable


@bp.route("/apps/<app_id>/payables", methods=["POST"])
@authorized
@use_args(
    {
        "display_name": fields.Str(required=True),
        "display_price": fields.Integer(required=True),
        "permalink": fields.Str(required=True),
    }
)
def create_payable(user, args, app_id):
    """
    Creates a new app for a given user
    """

    app = App.query.get(app_id)

    if app is None:
        raise ApiException("App does not exist", 400)

    payable = Payable(
        display_name=args["display_name"],
        display_price=args["display_price"],
        permalink=args["permalink"],
        app=app,
    )

    db.session.add(payable)
    db.session.commit()

    return payable

