from flask import Blueprint

bp = Blueprint("resources", __name__)

import backend.services.resources.payable