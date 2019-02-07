from flask import jsonify
from backend.services.health import bp


@bp.route('/health')
def health_check():
    return jsonify({'status': 'ok'}), 200
