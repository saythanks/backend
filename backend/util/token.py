from firebase_admin import auth


def validate(token):
    # try:
    decoded_token = auth.verify_id_token(token)
    # except:
    # return None

    return decoded_token
