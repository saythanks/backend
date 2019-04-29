import sys
import stripe
from flask import jsonify, request
from webargs import fields
from webargs.flaskparser import use_args

from ...persistence.db import db
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


@bp.route("/me/billing", methods=["POST"])
@authorized
@use_args({"cardToken": fields.Str(required=True), "name": fields.Str(required=True)})
def update_billing(user, args):

    if user.stripe_id is not None:
        customer = stripe.Customer.modify(
            user.stripe_id, source=args["cardToken"], name=args["name"]
        )
    else:
        customer = stripe.Customer.create(
            source=args["cardToken"], email=user.email, name=args["name"]
        )

    user.as_stripe_customer(customer)

    user.name = args["name"]

    db.session.commit()

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
    token = args["token"] if "token" in args.keys() else None
    amount = args["amount"]

    # balance = int(redis_client.get("balance", default=0))
    # balance += amount

    # redis_client.set("balance", balance)

    if token is not None and user.stripe_id is None:
        customer = stripe.Customer.create(
            source=token, email=user.email, name=user.name
        )
        if customer is None:
            raise ApiException("Could not create customer")
        user.as_stripe_customer(customer)

    cust_id = user.stripe_id

    if cust_id is None:
        raise ApiException("No token or payment source", status_code=400)

    deposit = user.deposit(amount)

    if deposit is None:
        raise ApiException("Could not complete payment")

    return jsonify({"balance": user.account.balance})

    # try:
    #     charge = stripe.Charge.create(
    #         amount=amount,
    #         currency="usd",
    #         description="Add to Account",
    #         customer=cust_id,
    #     )
    #     user.deposit(amount, token)
    #     return jsonify({"balance": user.account.balance, "charge": charge})
    # except stripe.error.CardError as e:
    #     msg = e.json_body["error"]["message"]
    #     raise ApiException(msg, status_code=e.https_status)
    # except Exception as e:
    #     print(e)
    #     raise ApiException("Problem Charging Card with Stripe")

