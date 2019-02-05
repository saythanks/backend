from flask import render_template, request

from backend.services.payments import bp


@bp.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if request.method is 'GET':
        return render_template("This would GET a transaction (given an id)")
    elif request.method is 'POST':
        return render_template("Just recevied " + request.get_data())
    else:
        return 'BAD HTTP METHOD'
