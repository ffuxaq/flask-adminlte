from flask import Blueprint

bp = Blueprint('stats_report', __name__)

from app.flask_adminlte.apps.authentication import models,routes