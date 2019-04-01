from webargs import fields
from webargs.flaskparser import use_args

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


@bp.route("/transactions", methods=["get"])
@authorized
@use_args({"app": fields.Str(), "page": fields.Integer(missing=1)})
def get_txs(user, args):
    dest_id = (
        App.query.get_or_404(args["app"]).account_id
        if "app" in args.keys()
        else user.account_id
    )

    page = args["page"]

    page_size = 20

    return Payment.payments_to(dest_id, page_size, page=page)


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
        "payable": fields.Str(required=True),
        "name": fields.Str(required=True),
        "email": fields.Str(required=True),
        "card_token": fields.Str(),
        "top_up": fields.Integer(),
    }
)
def create_tx_account(args):
    payable = Payable.query.get_or_404(args["payable"])

    user = User.create_for_email(args["email"], args["name"])
    if user is None:
        raise ApiException("Could not create user account")

    if "card_token" in args.keys():
        deposit = user.deposit(args["top_up"], args["card_token"])
        if deposit is None:
            raise ApiException("Could not deposit funds")

    payment = Payment.transfer(user, payable)
    if payment is None:
        raise ApiException("Could not complete transfer")

    return {"success": True}

