from flask import session, jsonify
from webargs import fields
from webargs.flaskparser import use_args

from backend.model.link import Link
from backend.services.tracker import bp
from backend.services.tracker.pixel import make_pixel_response

create_args = {'token': fields.Str(required=True)}


@bp.route('/tracker', methods=['GET'])
@use_args(create_args)
def create(args):
    """
    Creates a new tracking link
    """

    token = args['token']
    uid = session.get('user_id')

    status = 200
    if uid is not None:
        Link.create(token, uid)
        status = 201

    return make_pixel_response(), status


@bp.route('/tracker/<token>', methods=['GET'])
def get(token):
    """
    Connects the tracking link
    :return: HTTP Reponse
    """

    uid = Link.query(token)

    try:
        decoded_token = auth.verify_id_token(token)
    except:
        return "nah bro"

    return jsonify(decoded_token)
