from functools import wraps

from flask import request

from backend.errors.ApiException import ApiException
from backend.model.user import User
from backend.util.token import validate


def authorized(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not "Authorization" in request.headers:
            raise ApiException("No Authorization Header present", status_code=401)
        data = request.headers["Authorization"]
        token = str.replace(str(data), "Bearer ", "")

        decoded_token, error = validate(token)
        if decoded_token is None:
            raise ApiException(
                "Invalid auth token",
                status_code=401,
                payload={"token": token, "errror": error},
            )

        user, err = User.for_token(decoded_token)
        if user is None:
            raise ApiException(
                "Unable to find or create user for token", status_code=500
            )

        return f(user, *args, **kwargs)

    return decorated_function


def maybe_authorized(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "Authorization" not in request.headers:
            return f(None, *args, **kwargs)

        data = request.headers["Authorization"]
        token = str.replace(str(data), "Bearer ", "")

        decoded_token, error = validate(token)
        if decoded_token is None:
            raise ApiException(
                "Invalid auth token",
                status_code=401,
                payload={"token": token, "error": error},
            )

        user, err = User.for_token(decoded_token)
        if user is None:
            raise ApiException(
                "Unable to find or create user for token", status_code=500
            )

        return f(user, *args, **kwargs)

    return decorated_function
