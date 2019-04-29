from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
import stripe


from backend.model.model import BaseModel
from backend.model.deposit import Deposit
from backend.persistence.db import db


class Account(BaseModel):
    balance = db.Column(db.Integer, default=0, nullable=False)

    def deposit(self, amount, customer_id):
        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            description="Deposit to account",
            customer=customer_id,
        )

        deposit = Deposit(account=self, amount=amount)
        if self.balance is None:
            self.balance = amount
        self.balance += amount
        db.session.add(deposit)
        db.session.commit()

        return deposit
