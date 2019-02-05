from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text

from backend import db


class Account(db.Model):
    id = db.Column(UUID, primary_key=True,
                   server_default=text("uuid_generate_v4()"))
    balance = db.Column(db.Integer)

    time_created = db.Column(db.DateTime(
        timezone=True), server_default=func.now(), nullable=False,)
    time_updated = db.Column(db.DateTime(timezone=True),
                             server_default=func.now(), onupdate=func.now(), nullable=False,)
