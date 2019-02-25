from sqlalchemy.dialects.postgresql import JSONB, UUID

from backend.model.model import BaseModel
from backend.persistence.db import db


class Withdrawal(BaseModel):
    account_id = db.Column(UUID, db.ForeignKey("account.id"))
    account = db.relationship("Account")

    amount = db.Column(db.Integer, default=0, nullable=False)
    real_amount = db.Column(db.Integer, default=0, nullable=False)

    stripe_id = db.Column(db.Text)
    stripe_data = db.Column(JSONB)
