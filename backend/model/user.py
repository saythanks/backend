from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text

from backend import db


class User(db.Model):
    id = db.Column(UUID, primary_key=True,
                   server_default=text("uuid_generate_v4()"))

    email = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)

    account_id = db.Column(UUID, db.ForeignKey('account.id'))
    account = db.relationship('Account')

    stripe_id = db.Column(db.Text)

    time_created = db.Column(db.DateTime(
        timezone=True), server_default=func.now(), nullable=False,)
    time_updated = db.Column(db.DateTime(timezone=True),
                             server_default=func.now(), onupdate=func.now(), nullable=False,)
