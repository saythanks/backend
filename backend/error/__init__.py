from flask import Blueprint

bp = Blueprint('error', __name__)

import backend.error.ApiException
