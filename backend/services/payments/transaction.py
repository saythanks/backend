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
@use_args({"app": fields.Str(), "page": fields.Integer()})
def get_txs_to(user, args):
    return get_payments(user, args)
    
@bp.route("/transactions/from", methods=["get"])
@authorized
@use_args({"app": fields.Str(), "page": fields.Integer()})
def get_txs_from(user, args):
    return get_payments(user, args, to=False)

def get_payments(user, args, to=True):
    account_id = App.query.get_or_404(args["app"]).account_id if "app" in args.keys() else user.account_id
    page = args["page"] if "page" in args.keys() else 1
    page_size = 20

    if to:
        return Payment.payments_to(account_id, page_size, page=page)
    else:
        return Payment.payments_from(account_id, page_size, page=page)


@bp.route("/transactions", methods=["post"])
@authorized
@use_args({"app": fields.Str(required=True), "amount": fields.Int(required=True)})
def create_tx(user, args):
    app = App.query.get_or_404(args["app"])

    payment = Payment.transfer(user, app, args["amount"])

    if payment is None:
        raise ApiException("Could not complete payment")

    return {"success": True}


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
        customer = strip.Customer.create(
            source=args["card_token"],
            email=user.email
        )
        user.as_stripe_customer(customer)
        deposit = user.deposit(args["top_up"], args["card_token"])
        if deposit is None:
            raise ApiException("Could not deposit funds")

    payment = Payment.transfer(user, payable)
    if payment is None:
        raise ApiException("Could not complete transfer")

    return {"success": True}

