from flask import jsonify
from backend.error import bp


class ApiException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@bp.app_errorhandler(ApiException)
def handle_app_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@bp.app_errorhandler(404)
def handle_app_404(error):
    return jsonify({'message': 'This route does not exist'}), 404
