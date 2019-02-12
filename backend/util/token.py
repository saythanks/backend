# from firebase_admin import auth
from backend.lib.token_verify.validator import check_headers


def validate(token):

    payload = check_headers(token)
    return payload, None
    # try:
    #     decoded_token = auth.verify_id_token(token)
    # except Exception as e:
    #     return None, str(e)

    # return decoded_token, None

    # return {'email': 'newman.oscar@gmail.com', 'name': 'Oscar Newman'}
