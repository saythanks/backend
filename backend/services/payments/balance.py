import sys
import stripe
from flask import jsonify, request
from webargs import fields
from webargs.flaskparser import use_args

from backend.persistence.redis import redis_client
from backend.middleware.token_auth import authorized
from backend.services.payments import bp
from backend.middleware.token_auth import authorized


# Handles route that retrieves a user's balance
@bp.route("/balance", methods=["GET"])
@authorized
def index(user):
    balance = int(redis_client.get("balance", default=0))
    return jsonify(
        {"me": user.id, "balance": user.account.balance, "monthly_spend": 1.50}
    )


# Handles route that retrieves a user's balance
@bp.route("/balance", methods=["POST"])
@authorized
@use_args({"token": fields.Str(required=True), "amount": fields.Integer(required=True)})
def create(user, args):
    token = args["token"]
    amount = args["amount"]

    # balance = int(redis_client.get("balance", default=0))
    # balance += amount

    # redis_client.set("balance", balance)

    charge = stripe.Charge.create(
        amount=amount, currency="usd", description="Add to Account", source=token
    )

    user.deposit(amount, token)

    return jsonify({"balance": user.account.balance, "charge": charge})
