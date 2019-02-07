from flask import Blueprint

bp = Blueprint('health', __name__)

import backend.services.health.routes
