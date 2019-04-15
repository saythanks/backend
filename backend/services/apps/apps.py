from webargs import fields
from webargs.flaskparser import use_args
from flask import jsonify

from backend.services.apps import bp
from backend.middleware.token_auth import authorized, maybe_authorized
from backend.model.app import App
from ...persistence.db import db
from ...errors.ApiException import ApiException


@bp.route("/apps", methods=["GET"])
@authorized
def listApps(user):
    return list(map(lambda app: app.app_info(), user.apps))


@bp.route("/apps/<id>", methods=["GET"])
@maybe_authorized
def get(user, id):
    app = App.query.get_or_404(id)

    # if user is not None and user.owns(id):
    return App.query.get(id).app_info()

    # else:
    #     return App.basic_info(id)


@bp.route("/apps", methods=["POST"])
@authorized
@use_args(
    {
        "name": fields.Str(required=True),
        "description": fields.Str(),
        "url": fields.Str(),
        "image": fields.Str(),
    }
)
def create(user, args):
    """
    Creates a new app for a given user
    """
    # return jsonify(user.apps)

    app = App.create_for_user(
        user,
        args["name"],
        description=args["description"],
        url=args["url"],
        image_url=args["image"],
    )

    return app


@bp.route("/apps/<id>", methods=["DELETE"])
@authorized
def delete_app(user, args):
    app = App.query.get(id)
    if app is None:
        raise ApiException("Not found", status_code=401)

    if not user.owns(app.id):
        raise ApiException("Not authorized", status_code=421)

    db.session.delete(app)
    db.session.commit()
