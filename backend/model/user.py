from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy

from backend.persistence.db import db
from backend.model.model import BaseModel
from backend.model.account import Account
from backend.model.appUser import AppUser


class User(BaseModel):

    email = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)

    account_id = db.Column(UUID, db.ForeignKey("account.id"))
    account = db.relationship("Account")

    # apps = db.relationship("AppUser", back_populates="user")
    apps = association_proxy("user_apps", "app", creator=lambda app: AppUser(app=app))

    stripe_id = db.Column(db.Text)

    @staticmethod
    def create(email, name):
        account = Account()
        user = User(email=email, name=name, account=account)

        db.session.add(account)
        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def for_token(decoded_token):
        """
        Given a decoded firebase token with fields 'email' and 'name', provides the user matching
        that email if it exists, or creates a new user.
        """
        email = decoded_token["email"]
        name = decoded_token["name"]

        if email is None or name is None:
            return None, False

        user = User.query.filter_by(email=email).first()
        if user is not None:
            return user, False

        return User.create(email, name)
