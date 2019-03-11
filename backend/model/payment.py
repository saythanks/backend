from sqlalchemy.dialects.postgresql import UUID

from backend.errors.ApiException import ApiException
from backend.model.model import BaseModel
from backend.model.account import Account
from backend.persistence.db import db


class Payment(BaseModel):
    source_account_id = db.Column(UUID, db.ForeignKey("account.id"))
    source_account = db.relationship("Account", foreign_keys=[source_account_id])

    dest_account_id = db.Column(UUID, db.ForeignKey("account.id"))
    dest_account = db.relationship("Account", foreign_keys=[dest_account_id])

    payable_id = db.Column(UUID, db.ForeignKey("payable.id"))
    payable = db.relationship("Payable")

    amount = db.Column(db.Integer, nullable=False, default=0)

    @staticmethod
    def transfer(user, payable):
        balance = user.account.balance
        if balance is None or balance < payable.display_price:
            raise ApiException("Not enough funds")
            return None

        amount = payable.display_price
        app = payable.app

        payment = Payment(
            source_account=user.account,
            dest_account=payable.app.account,
            payable=payable,
            amount=payable.display_price,
        )

        user.account.balance -= amount

        if app.account.balance is None:
            app.account.balance = 0
        app.account.balance += amount

        db.session.add(payment)
        db.session.commit()

        return payment

