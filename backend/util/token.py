from firebase_admin import auth


def validate(token):
    try:
        decoded_token = auth.verify_id_token(token)
    except Exception as e:
        return None, str(e)

    return decoded_token, None

    # return {'email': 'newman.oscar@gmail.com', 'name': 'Oscar Newman'}
