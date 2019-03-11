from webargs import fields
from webargs.flaskparser import use_args

from backend.errors.ApiException import ApiException
from backend.middleware.token_auth import maybe_authorized, authorized
from backend.model.payable import Payable
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


@bp.route("/transactions", methods=["post"])
@authorized
@use_args({"payable": fields.Str(required=True)})
def create_tx(user, args):
    payable = Payable.query.get_or_404(args["payable"])

    payment = Payment.transfer(user, payable)

    if payment is None:
        raise ApiException("Could not complete payment")

    return {"success": True}


@bp.route("/transactions/new", methods=["post"])
@use_args(
    {
        "payable": fields.Str(required=True),
        "name": fields.Str(required=True),
        "email": fields.Str(required=True),
        "card_token": fields.Str(required=True),
        "top_up": fields.Integer(default=0),
    }
)
def create_tx_account(args):
    payable = Payable.query.get_or_404(args["payable"])

    user = User.create_for_email(args["email"], args["name"])
    if user is None:
        raise ApiException("Could not create user account")

    deposit = user.deposit(args["top_up"], args["card_token"])
    if deposit is None:
        raise ApiException("Could not deposit funds")

    payment = Payment.transfer(user, payable)
    if payment is None:
        raise ApiException("Coudl not complete transfer")

    return {"success": True}

