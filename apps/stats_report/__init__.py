from flask import Blueprint

bp = Blueprint('stats_report', __name__)

from apps.authentication import models,routes