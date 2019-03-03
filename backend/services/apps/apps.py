from webargs import fields
from webargs.flaskparser import use_args
from flask import jsonify

from backend.services.apps import bp
from backend.middleware.token_auth import authorized
from backend.model.app import App


@bp.route("/apps", methods=["GET"])
@authorized
def list(user):
    return user.apps.copy()


@bp.route("/apps/:id", methods=["GET"])
def get(user):
    pass


@bp.route("/apps", methods=["POST"])
@authorized
@use_args(
    {
        "name": fields.Str(required=True),
        "description": fields.Str(),
        "url": fields.Str(),
    }
)
def create(user, args):
    """
    Creates a new app for a given user
    """
    # return jsonify(user.apps)

    app = App.create_for_user(
        user, args["name"], description=args["description"], url=args["url"]
    )

    return app

