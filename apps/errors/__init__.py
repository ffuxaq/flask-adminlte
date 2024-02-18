from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.flask_adminlte.apps.errors import handlers