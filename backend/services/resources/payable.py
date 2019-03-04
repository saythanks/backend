from webargs import fields
from webargs.flaskparser import use_args

from flask import jsonify, request
from backend.services.resources import bp
from backend.middleware.token_auth import authorized
from backend.model.payable import Payable

@bp.route('/payable', methods=['GET'])
@authorized
@use_args({'id': fields.Str(required=True)})
def index(payable):
    p = Payable.with_id(payable.id)
    app = p.get_app()
    return jsonify({"name": p.name, "link": p.permalink,
                    "price": p.price, "app": {
                        "name": app.name
                        "id": app.id
                    }})

@bp.route('/payable', methods=['POST'])
@authorized
@use_args({'id': fields.Str(required=True)})
def create(payable):
    Payable.create(payable.name, payable.price, payable.type, payable.app_id, payable.permalink)
    return ""
