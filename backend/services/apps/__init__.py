from flask import Blueprint

bp = Blueprint("apps", __name__)

import backend.services.apps.apps
import backend.services.apps.payables
