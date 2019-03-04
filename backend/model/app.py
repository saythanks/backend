import random
import string

from flask import jsonify

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy


from backend.model.model import BaseModel
from backend.model.account import Account
from backend.model.appUser import AppUser
from backend.model.payable import Payable
from backend.persistence.db import db


class App(BaseModel):
    account_id = db.Column(UUID, db.ForeignKey("account.id"))
    account = db.relationship("Account")

    # users = db.relationship("AppUser", back_populates="app")
    users = association_proxy(
        "app_users", "user", creator=lambda user: AppUser(user=user)
    )

    payables = db.relationship("Payable", back_populates="app")

    secret = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)

    stripe_account_id = db.Column(db.Text, nullable=True)

    @staticmethod
    def generate_secret():
        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(40)
        )

    @staticmethod
    def create_for_user(user, name, url=None, description=None):
        account = Account()
        app = App(
            account=account,
            name=name,
            secret=App.generate_secret(),
            url=url,
            description=description,
        )

        user.apps.append(app)

        db.session.add(account)
        db.session.add(app)
        db.session.commit()

        return app

    @staticmethod
    def basic_info(id):
        # returns a publicly viewable dict containing basic info about app given an id
        app = App.get(id)
        return {"name", app.name, "url", app.url, "description", app.description}