import sys
import stripe
from flask import jsonify, request
from webargs import fields
from webargs.flaskparser import use_args

from backend.persistence.redis import redis_client
from backend.middleware.token_auth import authorized
from backend.services.payments import bp
from backend.middleware.token_auth import authorized
from backend.errors.ApiException import ApiException

from backend.model.payment import Payment


@bp.route("/me", methods=["GET"])
@authorized
def user_manifest(user):
    # We want: balance, transactions

    return {"me": user.to_dict(), "balance": user.account.balance}


# Handles route that retrieves a user's balance
@bp.route("/balance", methods=["GET"])
@authorized
def index(user):
    return jsonify(
        {"me": user.id, "balance": user.account.balance, "monthly_spend": 1.50}
    )


# Handles route that retrieves a user's balance
@bp.route("/balance", methods=["POST"])
@authorized
@use_args({"token": fields.Str(), "amount": fields.Integer(required=True)})
def create(user, args):
    token = args["token"]
    amount = args["amount"]

    # balance = int(redis_client.get("balance", default=0))
    # balance += amount

    # redis_client.set("balance", balance)

    # if token is not None and user.stripe_id is None:
    #     customer = stripe.Customer.create(source=token, email=user.email)
    #     user.as_stripe_customer(customer)

    # if token is None and user.stripe_id is not None:
    #     token = user.stripe_id

    # if token is None
    #     raise ApiException('No token or payment source', status_code=400)

    charge = stripe.Charge.create(
        amount=amount, currency="usd", description="Add to Account", source=token
    )

    user.deposit(amount, token)

    return jsonify({"balance": user.account.balance, "charge": charge})
