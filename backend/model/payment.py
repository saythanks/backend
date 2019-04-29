from datetime import datetime, timedelta

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import desc, func

from backend.errors.ApiException import ApiException
from backend.model.model import BaseModel
from backend.model.account import Account
from backend.model.app import App
from backend.model.user import User
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

    def get_user_info(self):
        d = BaseModel.to_dict(self)
        d["app"] = App.for_account(self.dest_account_id).to_dict()
        d["user"] = User.for_account(self.source_account_id).to_dict()
        return d

    @staticmethod
    def payments_to(dest_id, page_size, page=1):
        return (
            Payment.query.filter_by(dest_account_id=dest_id)
            .order_by(Payment.time_created.desc())
            .paginate(page, page_size, error_out=False)
        )

    @staticmethod
    def payments_from(source_id, page_size, page=1):
        return (
            Payment.query.filter_by(source_account_id=source_id)
            .order_by(Payment.time_created.desc())
            .paginate(page, page_size, error_out=False)
        )

    @staticmethod
    def payments_summary_to(dest_id):
        return (
            # Payment.query(Payment.time_created, func.sum(Payment.amount).label('total'))

            Payment.query.filter_by(dest_account_id=dest_id)
            # .group_by(func.day(Payment.time_created))
            .order_by(Payment.time_created.desc())
            .all()
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

        # Check if there is a matching payment in the last 15 minutes
        since = datetime.now() - timedelta(minutes=15)
        existing = (
            Payment.query.filter(Payment.time_created > since)
            .filter_by(source_account_id=user.account.id)
            .filter_by(dest_account_id=app.account.id)
            .order_by(Payment.time_created.desc())
            .first()
        )
        if existing is None:
            payment = Payment(
                source_account=user.account, dest_account=app.account, amount=amount
            )
            db.session.add(payment)

        else:
            existing.amount += amount
            existing.time_created = datetime.now()
            payment = existing

        user.account.balance -= amount

        if app.account.balance is None:
            app.account.balance = 0
        app.account.balance += amount

        db.session.commit()

        leftover = (price * count) - amount
        return payment, leftover

