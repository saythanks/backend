from functools import wraps
from flask import request, jsonify

from backend.model.user import User
from backend.util.token import validate
from backend.errors.ApiException import ApiException


def authorized(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'Authorization' in request.headers:
            raise ApiException(
                'No Authorization Header present', status_code=401)
        data = request.headers['Authorization']
        token = str.replace(str(data), 'Bearer ', '')

        decoded_token, error = validate(token)
        if decoded_token is None:
            raise ApiException(
                'Invalid auth token', status_code=401, payload={'token': token, 'errror': error})

        user = User.for_token(decoded_token)
        if user is None:
            raise ApiException(
                'Unable to find or create user for token', status_code=500)

        return f(user, *args, **kwargs)
    return decorated_function
