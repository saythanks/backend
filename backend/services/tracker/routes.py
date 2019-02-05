from flask import request, session
from flask_restful import reqparse

from backend.model.link import Link
from backend.services.tracker import bp
from backend.services.tracker.pixel import make_pixel_response


@bp.route('/tracker', methods=['GET'])
def create():
    """
    Creates a new tracking link
    """

    parser = reqparse.RequestParser()
    parser.add_argument('token', required=True,
                        help='UUID token must be supplied')
    args = parser.parse_args()

    token = args['token']
    uid = session.get('user_id')

    status = 200
    if uid is not None:
        Link.create(token, uid)
        status = 201

    return make_pixel_response(), status
