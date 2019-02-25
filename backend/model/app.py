from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text

from backend.persistence.db import db
from backend.model.model import BaseModel
from backend.model.account import Account

association_table = db.Table(
    "app_user",
    BaseModel.metadata,
    db.Column("app_id", UUID, db.ForeignKey("app.id")),
    db.Column("user_id", UUID, db.ForeignKey("user.id")),
)


class App(BaseModel):

    account_id = db.Column(UUID, db.ForeignKey("account.id"))
    account = db.relationship("Account")

    users = db.relationship("User", secondary=association_table, backref="apps")

    secret = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
