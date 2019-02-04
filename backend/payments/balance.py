import functools
from flask import request, render_template, jsonify
from flask_cors import cross_origin
import stripe
from backend.payments import bp

from backend import balance


# Handles route that retrieves a user's balance
@bp.route('/balance', methods=['GET'])
def index():

    return jsonify({'balance': balance, 'monthly_spend': 1.50})

# Handles route that retrieves a user's balance
@bp.route('/balance', methods=['POST'])
@cross_origin()
def create():
	stripe.api_key = "sk_test_ssrVf0FK8RDjJVrPozoWT1iq"
	json = request.get_json()
	token = json['token']
	amount = json['amount']

	balance += amount

	charge = stripe.Charge.create(
		amount=amount,
		currency='usd',
		description='Add to Account',
		source=token
	)


	return jsonify({ 'charge': 3 })