from urllib.request import urlopen
import json

from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from jose import jwt

from backend.errors.ApiException import ApiException


def load_keys():
    json_url = urlopen(
        'https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com')
    keys = json.loads(json_url.read())

    for kid, key in keys.items():
        cert_str = key.encode()
        cert_obj = load_pem_x509_certificate(cert_str, default_backend())
        public_key = cert_obj.public_key()
        keys[kid] = public_key

    return keys


def check_headers(token):

    keys = load_keys()
    unverified_header = jwt.get_unverified_header(token)

    if unverified_header['alg'] != 'RS256':
        raise ApiException('Invalid token, algorithm is not RS256')

    try:
        payload = jwt.decode(
            token,
            keys,
            algorithms=['RS256'],
            audience='micro-pay-me',
            issuer='https://securetoken.google.com/micro-pay-me'
        )

    except jwt.ExpiredSignatureError:
        raise ApiException({
            'code': 'token_expired',
            'description': 'Token expired.'
        }, 401)

    except jwt.JWTClaimsError:
        raise ApiException({
            'code': 'invalid_claims',
            'description': 'Incorrect claims. Please, check the audience and issuer.'
        }, 401)
    except Exception as e:
        raise ApiException({
            'code': 'invalid_header',
            'description': 'Unable to parse authentication token.',
            'error': str(e)
        }, 400)

    return dict(payload)
