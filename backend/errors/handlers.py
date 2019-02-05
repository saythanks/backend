from flask import jsonify

from backend.errors import bp
from backend.errors.ApiException import ApiException
from backend.errors.jsonError import error_response as api_error_response
from backend.persistence import db


@bp.app_errorhandler(ApiException)
def handle_app_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@bp.app_errorhandler(404)
def not_found_error(error):
    return api_error_response(404, message='Thais route does not exist')


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return api_error_response(500)
