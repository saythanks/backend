import functools
from flask import request, render_template, jsonify
from backend.payments import bp

# Handles route that retrieves a user's balance
@bp.route('/balance', methods=['GET'])
def balance():
    return jsonify({'balance': 13.25, 'monthly_spend': 1.40})