from webargs import fields, validate
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

@bp.route("/transactions/to/summary", methods=["get"])
@authorized
@use_args({"app": fields.Str(required=True)})
def get_tx_summary_to(user, args):
    app = App.query.get_or_404(args["app"])

    return {
        "items": [15, 12, 5, 9, 24]
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

def get_payments_summary(account_id, to=True):
    if to:
        return Payment.payments_summary_to(account_id)


@bp.route("/transactions", methods=["post"])
@authorized
@use_args(
    {
        "app": fields.Str(required=True),
        "price": fields.Int(required=True, validate=validate.Range(min=0, max=100)),
        "count": fields.Int(missing=1, validate=validate.Range(min=0, max=10)),
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
        "price": fields.Int(required=True, validate=validate.Range(min=0, max=100)),
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
        deposit = user.deposit(args["top_up"])
        if deposit is None:
            raise ApiException("Could not deposit funds")

    payment = Payment.transfer(user, app, args["price"], 1)
    if payment is None:
        raise ApiException("Could not complete transfer")

    return {"success": True}

