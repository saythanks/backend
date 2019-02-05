from flask import Blueprint

bp = Blueprint('service.tracking', __name__)

import backend.services.tracker.routes
