from flask import request, render_template, jsonify, current_app
from flask_cors import cross_origin
import stripe
from backend.payments import bp
from backend.persistence.redis import redis_client


# Handles route that retrieves a user's balance
@bp.route('/balance', methods=['GET'])
def index():
    balance = int(redis_client.get('balance', default=0))
    return jsonify({'balance': balance, 'monthly_spend': 1.50})


# Handles route that retrieves a user's balance
@bp.route('/balance', methods=['POST'])
def create():
    stripe.api_key = "sk_test_ssrVf0FK8RDjJVrPozoWT1iq"
    json = request.get_json()
    token = json['token']
    amount = json['amount']

    balance = int(redis_client.get('balance', default=0))
    balance += amount

    redis_client.set('balance', balance)

    charge = stripe.Charge.create(
        amount=amount,
        currency='usd',
        description='Add to Account',
        source=token
    )

    return jsonify({'balance': balance, 'charge': charge})
