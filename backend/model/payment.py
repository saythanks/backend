from sqlalchemy.dialects.postgresql import UUID

from backend.model.model import BaseModel
from backend.persistence.db import db


class Payment(BaseModel):
    source_account_id = db.Column(UUID, db.ForeignKey("account.id"))
    source = db.relationship("Account")

    dest_account_id = db.Column(UUID, db.ForeignKey("account.id"))
    dest_account = db.relationship("Account")

    payable_id = db.Column(UUID, db.ForeignKey("payable.id"))
    payable = db.relationship("Payable")

    amount = db.Column(db.Integer, nullable=False, default=0)
