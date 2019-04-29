from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
import stripe


from backend.model.model import BaseModel
from backend.model.deposit import Deposit
from backend.persistence.db import db
from backend.errors.ApiException import ApiException


class Account(BaseModel):
    balance = db.Column(db.Integer, default=0, nullable=False)

    def deposit(self, amount, customer_id):
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                description="Deposit to account",
                customer=customer_id,
            )

            deposit = Deposit(account=self, amount=amount)
            if self.balance is None:
                self.balance = amount
            self.balance += amount
            db.session.add(deposit)
            db.session.commit()

            return deposit
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            msg = e.json_body["error"]["message"]
            raise ApiException(msg, status_code=e.https_status)
        # except stripe.error.RateLimitError as e:
        #   # Too many requests made to the API too quickly
        #   pass
        # except stripe.error.InvalidRequestError as e:
        #   # Invalid parameters were supplied to Stripe's API
        #   pass
        # except stripe.error.AuthenticationError as e:
        #   # Authentication with Stripe's API failed
        #   # (maybe you changed API keys recently)
        #   pass
        # except stripe.error.APIConnectionError as e:
        #   # Network communication with Stripe failed
        #   pass
        # except stripe.error.StripeError as e:
        #   # Display a very generic error to the user, and maybe send
        #   # yourself an email
        #   pass
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            return None
