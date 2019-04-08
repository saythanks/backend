from webargs import fields
from webargs.flaskparser import use_args
import stripe

from backend.errors.ApiException import ApiException
from backend.middleware.token_auth import maybe_authorized, authorized
from backend.model.payable import Payable
from backend.model.app import App
from backend.model.payment import Payment
from backend.model.account import Account
from backend.model.deposit import Deposit
from backend.model.user import User
from backend.services.payments import bp

"""
If signed in:
- payable_id


If not signed in:
- payable_id
- name
- email
- card_token
- top_up
"""


@bp.route("/transactions/to", methods=["get"])
@authorized
@use_args({"app": fields.Str(required=True), "page": fields.Integer(missing=1)})
def get_txs_to(user, args):
    app = App.query.get_or_404(args["app"])
    pg = get_payments(app.account_id, args["page"], to=True)

    return {
        "items": list(map(lambda i: i.get_user_info(), pg.items)),
        "total": pg.total,
        "has_next": pg.has_next,
        "has_prev": pg.has_prev,
        "next_num": pg.next_num,
        "prev_num": pg.prev_num,
    }


@bp.route("/transactions/from", methods=["get"])
@authorized
@use_args({"app": fields.Str(), "page": fields.Integer(missing=1)})
def get_txs_from(user, args):
    pg = get_payments(user.account_id, args["page"], to=False)

    return {
        "items": list(map(lambda i: i.get_user_info(), pg.items)),
        "total": pg.total,
        "has_next": pg.has_next,
        "has_prev": pg.has_prev,
        "next_num": pg.next_num,
        "prev_num": pg.prev_num,
    }


def get_payments(account_id, page, to=True):
    page_size = 5

    if to:
        return Payment.payments_to(account_id, page_size, page=page)
    else:
        return Payment.payments_from(account_id, page_size, page=page)


2


@bp.route("/transactions", methods=["post"])
@authorized
@use_args(
    {
        "app": fields.Str(required=True),
        "price": fields.Int(required=True),
        "count": fields.Int(missing=1),
    }
)
def create_tx(user, args):
    app = App.query.get_or_404(args["app"])

    payment, leftover = Payment.transfer(user, app, args["price"], args["count"])

    if payment is None:
        raise ApiException("Could not complete payment")

    return {
        "success": True,
        "notProcessed": leftover,
        "paid": payment.amount,
        "balance": user.account.balance,
    }


@bp.route("/transactions/new", methods=["post"])
@use_args(
    {
        "app": fields.Str(required=True),
        "price": fields.Int(required=True),
        "name": fields.Str(required=True),
        "email": fields.Str(required=True),
        "card_token": fields.Str(),
        "top_up": fields.Integer(),
    }
)
def create_tx_account(args):
    app = App.query.get_or_404(args["app"])

    user = User.create_for_email(args["email"], args["name"])
    if user is None:
        raise ApiException("Could not create user account")

    if "card_token" in args.keys():
        customer = stripe.Customer.create(source=args["card_token"], email=user.email)
        user.as_stripe_customer(customer)
        deposit = user.deposit(args["top_up"], args["card_token"])
        if deposit is None:
            raise ApiException("Could not deposit funds")

    payment = Payment.transfer(user, app, args["price"], 1)
    if payment is None:
        raise ApiException("Could not complete transfer")

    return {"success": True}

