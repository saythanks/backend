from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy


from backend.errors.ApiException import ApiException
from backend.persistence.db import db
from backend.model.model import BaseModel
from backend.model.account import Account
from backend.model.appUser import AppUser


class User(BaseModel):

    email = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=True)

    account_id = db.Column(UUID, db.ForeignKey("account.id"))
    account = db.relationship("Account")

    # apps = db.relationship("AppUser", back_populates="user")
    apps = association_proxy("user_apps", "app", creator=lambda app: AppUser(app=app))

    stripe_id = db.Column(db.Text)
    last_4 = db.Column(db.Text)
    card_brand = db.Column(db.Text)

    top_up = db.Column(db.Integer, default=0, nullable=True)

    def owns(self, app_id):
        return id in [app.id for app in self.apps]

    @staticmethod
    def create(email, name, commit=True):
        account = Account()
        user = User(email=email, name=name, account=account)

        db.session.add(account)
        db.session.add(user)

        if commit:
            db.session.commit()

        return user

    def as_stripe_customer(self, customer, commit=True):
        # takes in a stripe customer object and sets fields of user accordingly
        if customer is not None:
            self.stripe_id = customer.stripe_id

            if len(customer.sources.data) > 0:
                self.last_4 = customer.sources.data[0].last4
                self.card_brand = customer.sources.data[0].brand

        if commit:
            db.session.commit()

        return self

    def deposit(self, amount):
        if self.stripe_id is None:
            return None

        return self.account.deposit(amount, self.stripe_id)

    @staticmethod
    def create_for_email(email, name):
        if email is None or name is None:
            return None

        user = User.query.filter_by(email=email).first()
        if user is not None:
            raise ApiException("User with this email already exists")

        return User.create(email, name, commit=False)

    @staticmethod
    def for_token(decoded_token):
        """
        Given a decoded firebase token with fields 'email' and 'name', provides the user matching
        that email if it exists, or creates a new user.
        """
        email = decoded_token["email"]
        name = decoded_token["name"] if "name" in decoded_token.keys() else None

        if email is None:
            return None, False

        user = User.query.filter_by(email=email).first()
        if user is not None:
            return user, False

        return User.create(email, name)

    @staticmethod
    def for_account(account_id):
        return User.query.filter_by(account_id=account_id).first()
