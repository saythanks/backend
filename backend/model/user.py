from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text

from backend.persistence.db import db
from backend.model.account import Account


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

    @staticmethod
    def create(email, name):
        account = Account()
        user = User(email=email,
                    name=name, account=account)

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
        email = decoded_token['email']
        name = decoded_token['name']

        if email is None or name is None:
            return None, False

        user = User.query.filter_by(email=email).first()
        if user is not None:
            return user, False

        return User.create(email, name)
