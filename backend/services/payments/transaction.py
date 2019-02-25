from webargs import fields
from webargs.flaskparser import use_args

from backend.errors.ApiException import ApiException
from backend.middleware.token_auth import authorized
from backend.model.payable import Payable
from backend.services.payments import bp


@bp.route('/transaction', methods=['post'])
@authorized
@use_args({'payable': fields.Str(required=True)})
def create_tx(args, user):
    payable = Payable.query.get(args['payable'])
    if payable is None:
        raise ApiException("Payable not found", status_code=400)

    pass
