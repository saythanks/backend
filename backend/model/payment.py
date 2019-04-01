from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import desc

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

    content_url = db.Column(db.String)

    amount = db.Column(db.Integer, nullable=False, default=0)

    @staticmethod
    def payments_to(dest_id, page_size, page=1):
        return (
            Payment.query.filter_by(dest_account_id=dest_id)
            .order_by(Payment.time_created.desc())
            .paginate(page, page_size, error_out=False)
        )

    @staticmethod
    def transfer(user, app, price, count):
        balance = user.account.balance
        leftover = 0

        amount = count * price

        if balance is None or balance < price:
            raise ApiException("Not enough funds")

        if balance < amount:
            # Get amount that can fit
            amount = (balance // price) * price

        payment = Payment(
            source_account=user.account, dest_account=app.account, amount=amount
        )

        user.account.balance -= amount

        if app.account.balance is None:
            app.account.balance = 0
        app.account.balance += amount

        db.session.add(payment)
        db.session.commit()

        leftover = (price * count) - payment.amount
        return payment, leftover

