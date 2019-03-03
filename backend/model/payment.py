from sqlalchemy.dialects.postgresql import UUID

from backend.model.model import BaseModel
from backend.persistence.db import db


class Payment(BaseModel):
    source_account_id = db.Column(UUID, db.ForeignKey("account.id"))
    source_account = db.relationship("Account", foreign_keys=[source_account_id])

    dest_account_id = db.Column(UUID, db.ForeignKey("account.id"))
    dest_account = db.relationship("Account", foreign_keys=[dest_account_id])

    payable_id = db.Column(UUID, db.ForeignKey("payable.id"))
    payable = db.relationship("Payable")

    amount = db.Column(db.Integer, nullable=False, default=0)
